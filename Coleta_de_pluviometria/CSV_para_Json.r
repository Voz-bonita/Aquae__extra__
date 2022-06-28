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
        ),
        na = c("-9999", NA)
    ) %>%
        na.omit() %>%
        rename_all(~ c("Data", "Chuva")) %>%
        mutate(Data = as.integer(str_sub(Data, start = 6, end = -4L))) %>%
        group_by(Data) %>%
        summarise("Acumulada" = sum(Chuva), "n_obs" = length(Chuva)) %>%
        mutate(Acumulada = (Acumulada + 1e-10) * (n_obs > 400))

    ans <- numeric(12)
    ans[res$Data] <- res$Acumulada
    ans[ans == 0] <- NA
    return(ans)
}


estados <- c(
    "AC", "AL", "AP", "AM", "BA", "CE",
    "DF", "ES", "GO", "MA", "MT", "MS",
    "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC",
    "SP", "SE", "TO"
)
df_json <- data(matrix(nrow = 10, ncol = 27)) %>%
    rename_all(~estados)

dir <- "Coleta_de_pluviometria/CSVs/"
csvs <- list.files(dir)
info <- str_split(csvs, "_")
codigo <- unique(map_chr(info, ~ .x[4]))

csvs_estacao <- csvs[str_detect(csvs, codigo[1])]
info_estacao <- str_split(csvs_estacao[1], "_")
uf <- info_estacao[3]
cidade <- info_estacao[5]


csv_path <- str_c("Coleta_de_pluviometria/CSVs/", csvs_estacao)
resultados <- map(csv_path, clean_vroom)

matrix(
    unlist(resultados, use.names = FALSE),
    ncol = length(csv_path), nrow = 12
) %>%
    rowQuantiles(probs = 0.5, na.rm = TRUE) %>%
    round(digits = 3)