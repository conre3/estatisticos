#' Pega todos os nomes dos estatisticos
#' 
#' @export
pega_nomes <- function() {
  link <- 'http://www.conre3.org.br/portal/?page_id=170'
  r <- httr::GET(link)
  h <- rvest::html(r)
  nodes <- rvest::html_nodes(h, xpath = '//div[@id="tab-01"]//span')
  stat <- rvest::html_text(nodes)
  stat <- stat[(grep('ESTATÍSTICOS', stat) + 1):(grep('TÉCNICOS', stat) - 1)]
  
  d <- dplyr::data_frame(nome = abjutils::rm_accent(stat))
  d <- dplyr::mutate(d, fl = primeiro_ultimo(nome),
                     primeiro = sapply(fl, function(x) {strsplit(x, ' ')[[1]][1]}),
                     ultimo = sapply(fl, function(x) {strsplit(x, ' ')[[1]][2]}))
  d
}

#' @export
get_pessoa <- function(nome) {
  nm <- strsplit(nome, ' ')[[1]]
  nm <- tolower(paste(nm[1], nm[length(nm)], sep = '.'))
  link <- sprintf('http://graph.facebook.com/%s', nm)
  r <- httr::GET(link)
  txt <- httr::content(r, 'text')
  d <- data.frame(jsonlite::fromJSON(txt), stringsAsFactors = FALSE)
  d <- dplyr::mutate_each(d, dplyr::funs(as.character))
  d$usr <- nm
  d
}

#' @export
my_ip <- function() {
  jsonlite::fromJSON(readLines("http://api.hostip.info/get_json.php", warn=F))$ip
}

#' @export
get_pessoas <- function(nomes) {
  d <- dplyr::data_frame(nome = nomes)
  d <- dplyr::group_by(d, nome)
  d <- dplyr::do(d, get_pessoa(.$nome))
  d <- dplyr::ungroup(d)
  d
}

#' @export
primeiro_ultimo <- Vectorize(FUN = function(nm) {
  spl <- strsplit(nm, ' ')[[1]]
  n <- length(spl)
  r <- paste(spl[1], spl[n])
  r
})

#' @export
pega_nomes_cea <- function(l) {
  # message(l)
  h <- xml2::read_html(httr::GET(l))
  x <- rvest::html_text(h)
  x <- gsub('[\n\r ]+', ' ', x)
  x <- abjutils::rm_accent(x)
  x <- stringr::str_split(x, 'Responsaveis pela analise estatistica: ')[[1]][-1]
  x <- stringr::str_split(x, 'Tecnicas estatisticas utili(li)?zadas:')
  x <- sapply(x, function(y) y[1])
  x <- stringr::str_split(x, ',|;| e ')
  x <- sapply(x, function(y) y[-1])
  x <- stringr::str_trim(unlist(x))
  unique(x)
}

#' @export
pega_cea <- function() {
  base <- 'http://www.ime.usp.br/~cea'
  h <- xml2::read_html(httr::GET(sprintf('%s/menusotao.html', base)))
  nodes <- rvest::html_nodes(h, xpath = '//select[@name="menusotao"]//option')
  links <- sprintf('%s/%s', base, rvest::html_attr(nodes, 'value'))
  d <- dplyr::data_frame(link = links)
  d <- dplyr::distinct(d, link, .keep_all = TRUE)
  d <- dplyr::group_by(d, link)
  d <- dplyr::do(d, nome = pega_nomes_cea(.$link))
  d <- dplyr::ungroup(d)
  d <- tidyr::unnest(d, nome)
  d <- dplyr::mutate(d, nome = abjutils::rm_accent(toupper(nome)),
                     nome = gsub(' +', ' ', nome),
                     nome = stringr::str_trim(gsub('[^A-Z ]', '', nome)),
                     fl = primeiro_ultimo(nome),
                     primeiro = sapply(fl, function(x) {strsplit(x, ' ')[[1]][1]}),
                     ultimo = sapply(fl, function(x) {strsplit(x, ' ')[[1]][2]}))
  d <- dplyr::mutate(d, ano = gsub('[^0-9]', '', link),
                     ano = paste0(ifelse(as.numeric(ano) > 20, '19', '20'), ano))
  d <- dplyr::arrange(d, desc(ano))
  d <- dplyr::select(d, -link)
  d <- dplyr::distinct(d, nome, .keep_all = TRUE)
  d <- dplyr::arrange(d, nome)
  d <- dplyr::rename(d, nome_cea = nome)
  dplyr::tbl_df(d)
}

#' @export
# get_google_um <- function(nm, ip, s) {
#   try({
#     Sys.sleep(s)
#     link <-  sprintf('https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s&userip=%s',
#                      URLencode(nm), ip)
#     r <- httr::GET(link)
#     h <- jsonlite::fromJSON(httr::content(r, 'text'))
#     d <- suppressWarnings(data.frame(h$responseData, stringsAsFactors = FALSE))
#     print(h$responseStatus)
#     return(d)
#   })
#   return(data.frame(status = 0))
# }

#' @export
get_google <- function(nomes, path) {
  a <- system.file('python/pyg.py', package = 'estatisticos')
  rPython::python.load(a)
  d <- dplyr::data_frame(nome = nomes)
  d <- dplyr::distinct(d, nome, .keep_all = TRUE)
  d <- dplyr::group_by(d, nome)
  d <- dplyr::do(d, get_google_um(.$nome, path))
  d <- dplyr::ungroup(d)
  rPython::python.exec('driver.close()')
  d
}

#' @export
get_google_um <- function(nm, path) {
  cat('\n', nm, '\n')
  try({
    rPython::python.call('pega_pessoa', tolower(nm), path)
#     arq <- gsub(' ', '_', tolower(nm))
#     arq <- sprintf('%s/%s.html', path, arq)
#     s <- file.info(arq)$size
#     if(s < 10000) {
#       file.remove(arq)
#       a <- system.file('python/pyg.py', package = 'estatisticos')
#       rPython::python.exec('driver.close()')
#       rPython::python.load(a)
#       rPython::python.call('pega_pessoa', tolower(nm), path)
#     }
  })
}


#' @export
# get_google_um <- function(nm, ip, s) {
#   try({
#     Sys.sleep(s)
#     link <-  sprintf('http://www.google.com/search?q=%s', URLencode(nm))
#     
#     httr::GET("http://google.com/", path = "search", query = list(q = "ham", hl='pt-br'))
#     
#     r <- httr::GET(link)
#     
#     cat(httr::content(r, 'text'))
#     
#     h <- jsonlite::fromJSON(httr::content(r, 'text'))
#     d <- suppressWarnings(data.frame(h$responseData, stringsAsFactors = FALSE))
#     cat(h$responseStatus)
#     return(d)
#   })
#   print(h)
#   return(data.frame(status = 0))
# }
