packages <- c(
    "dplyr", "vroom", "stringr",
    "magrittr", "tidyr", "purrr",
    "matrixStats", "foreach", "doParallel",
    "rjson"
)
pacman::p_load(packages, character.only = TRUE)


n_cores <- parallel::detectCores() - 1
my_cluster <- parallel::makeCluster(
    n_cores,
    type = "PSOCK"
)

doParallel::registerDoParallel(cl = my_cluster)

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
        mutate(Data = as.integer(
            stringr::str_sub(Data, start = 6, end = -4L)
        )) %>%
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
        ~ stringr::str_sub(.x[6], start = 7L)
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

dir <- "Coleta_de_pluviometria/CSVs/"
csvs <- list.files(dir)
info <- str_split(csvs, "_")

codigo <- unique(map_chr(info, ~ .x[4]))
codigo_cidade <- map_chr(codigo, ~ info[which(str_detect(csvs, .x))][[1]][5])
codigo_uf <- map_chr(codigo, ~ info[which(str_detect(csvs, .x))][[1]][3])

pluv_br <- foreach(
    i = 1:27,
    .packages = packages
) %dopar% {
    uf <- estados[i]
    map(
        codigo[codigo_uf == uf],
        ~ clean_resultados(csvs, .x)
    ) %>%
        magrittr::set_names(codigo_cidade[codigo_uf == uf])
}
pluv_br <- magrittr::set_names(pluv_br, estados)

for (uf in names(pluv_br)) {
    for (estacao in names(pluv_br[[uf]])) {
        validacao <- matrix(
            unlist(pluv_br[[uf]][[estacao]]),
            nrow = 12, ncol = length(pluv_br[[uf]][[estacao]])
        )
        decisao <- any(apply(validacao, 1, function(x) sum(x != 0) <= 3))
        if (decisao) pluv_br[[uf]][[estacao]] <- NULL
    }
}
for (uf in names(pluv_br)) {
    for (estacao in names(pluv_br[[uf]])) {
        for (ano in names(pluv_br[[uf]][[estacao]])) {
            pluv_br[[uf]][[estacao]][[ano]] <- round(
                pluv_br[[uf]][[estacao]][[ano]], 3
            )
        }
    }
}
export <- rjson::toJSON(pluv_br, indent = 0, method = "C")
write(export, file = "Coleta_de_pluviometria/Pluviometria_Brasil.json")