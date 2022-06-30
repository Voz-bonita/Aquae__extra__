pacman::p_load(
    "dplyr", "vroom", "stringr",
    "magrittr", "tidyr", "purrr",
    "matrixStats"
)


clean_vroom <- function(data) {
    res <- vroom(
        data,
        delim = ";", skip = 8,
        col_select = c(1, 3),
        show_col_types = FALSE,
        locale = locale(
            grouping_mark = ".",
            decimal_mark = ",",
            encoding = "ISO-8859-2"
        )
    ) %>%
        rename_all(~ c("Data", "Chuva")) %>%
        filter(Chuva != -9999) %>%
        mutate(Data = as.integer(str_sub(Data, start = 6, end = -4L))) %>%
        group_by(Data) %>%
        summarise("Acumulada" = sum(Chuva), "n_obs" = length(Chuva)) %>%
        mutate(Acumulada = (Acumulada + 1e-10) * (n_obs > 400))

    ans <- numeric(12)
    ans[res$Data] <- res$Acumulada
    return(as.list(ans))
}


clean_resultados <- function(csvs, estacao) {
    csvs_estacao <- csvs[stringr::str_detect(csvs, estacao)]
    anos <- purrr::map_chr(
        stringr::str_split(csvs_estacao, "_"),
        ~ str_sub(.x[6], start = 7L)
    )

    csv_path <- stringr::str_c("Coleta_de_pluviometria/CSVs/", csvs_estacao)
    resultados <- purrr::map(csv_path, clean_vroom)
    names(resultados) <- anos

    return(resultados)
}


estados <- c(
    "AC", "AL", "AP", "AM", "BA", "CE",
    "DF", "ES", "GO", "MA", "MT", "MS",
    "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC",
    "SP", "SE", "TO"
)

json <- map(estados, ~ list())
names(json) <- estados

dir <- "Coleta_de_pluviometria/CSVs/"
csvs <- list.files(dir)
info <- str_split(csvs, "_")

codigo <- unique(map_chr(info, ~ .x[4]))
codigo_hash <- map_chr(codigo, ~ info[which(str_detect(csvs, .x))][[1]][5])

json <- map(codigo[1:2], ~ clean_resultados(csvs, .x)) %>%
    magrittr::set_names(codigo_hash[1:2])

c("a", "b", "c") %>%
    purrr::set_names()