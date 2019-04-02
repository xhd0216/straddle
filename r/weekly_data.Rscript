library('tseries')
library('optparse')
library('yaml')

assert <- function(x) {
  stopifnot(isTRUE(x))
}


wp <- function(df, cutoff = 'weeks') {
  dates = row.names(df)
  weeks = cut(as.Date(dates), cutoff)
  dw = data.frame(df, Weeks = weeks)

  ret = data.frame(matrix(ncol=4, nrow=0))
  colnames(ret) = c('Open', 'High', 'Low', 'Close')
  for (w in unique(weeks)) {
    ss = dw[dw$Weeks == w,]
    ret[w, ] = c(ss[1, ]$Open, max(ss$High), min(ss$Low), ss[nrow(ss), ]$Close)
  }
  return(ret)
}


wpc <- function(df, cutoff = 'weeks', quote = 'Close') {
  ret = wp(df, cutoff = cutoff)
  rn = row.names(ret)
  ret = ret[quote]
  row.names(ret) = rn
  return(ret)
}


stock.return <- function(closes) {
  # not used for single stock
  return(data.frame(diff(as.matrix(closes))) / closes[-nrow(closes), ])
}


stock.vol <- function(closes, days_in_year=250) {
  ## don't use stock.return,dd this is only for single stock
  ret = diff(as.matrix(closes)) / closes[-length(closes)]
  #ret = stock.return(closes)
  vol = sd(ret) * sqrt(days_in_year)
  return(vol)
}


stock.downloads <- function(tik, start, end) {
  dat = get.hist.quote(instrument = tik, start = start)
  return(data.frame(dat))
}

stock.corr.helper <- function(all_closes) {
  close.returns = stock.return(all_closes)
  return(corr(close.returns))
}

stock.corr <- function(
    symbols,
    start ='1993-01-01',
    end = '2099-12-31',
    period = 'days',
    quote = 'Close',
    cache = TRUE
) {
  # download data
  all_closes = stock.loads(symbols, start.date = start, end.date = end, cache = cache, period = period, quote = quote)
  return(stock.corr.helper(all_closes))
}

read.cache <- function(fn, start, end, allow_gap) {
  df = read.csv(fn, row.names = 1)
  das = row.names(df)
  std = as.Date(head(das, 1))
  edd = as.Date(tail(das, 1))
  cat(paste0("loaded data\nstart = ", std, 
      " looking for = ", start,
      "\nend = ", edd,
      " looking for = ", end, "\n")
  )
  assert(!(std - as.Date(start) > allow_gap || as.Date(end) - edd > allow_gap))
  return(df)
}


download <- function(
    tik = 'spy',
    start = '2017-01-01',
    end = Sys.Date(),
    cache = TRUE,
    allow_gap = 5
) {
  fname = paste0(tik, '_data.csv')
  is.done = FALSE
  cat("trying to load", tik, "from cache\n")
  if (cache) {
    tryCatch(
        {
          df = read.cache(fname, start, end, allow_gap);
          is.done = TRUE;
          print("get from cache")
        },
        warning = function(w) {},
        error = function(e) {},
        finally = {}
    )
  }
  if (!is.done) {
    dat = get.hist.quote(instrument = tik, start = start)
    df = data.frame(dat)
    write.csv(df, file = paste0(tik, '_data.csv'))
    print("get from web")
  }

  return(df[row.names(df) >= start & row.names(df) <= end, ])
}


get.between.dates <- function(data, start, end) {
  return(data[row.names(data) >= start & row.names(data) <= end, ])
}


corr <- function(df) {
  nc = ncol(df)
  ret.matrix = matrix(, nrow = nc, ncol = nc)

  for (i in 1:nc) {
    for (j in 1:nc) {
      ret.matrix[i, j] = ret.matrix[j, i] = cor(unlist(df[i]), unlist(df[j]))
    }
  }
  row.names(ret.matrix) = colnames(df)
  colnames(ret.matrix) = colnames(df)
  ret = data.frame(ret.matrix)
  return(ret.matrix)
}

stock.loads <- function(
    syms, start.date = '2018-01-01', end.date = Sys.Date(), cache = TRUE,
    period = 'days', quote = 'Close'
) {
  ns = length(syms)
  all_closes = NULL
  for (n in 1:ns) {
    s = syms[n]
    da = download(tik = s, start = start.date, cache = cache)
    da = wpc(da, period, quote)
    colnames(da) <- c(s)
    if (n == 1) {
      all_closes = da
    }
    else {
      all_closes = merge(all_closes, da, by = 0)
      row.names(all_closes) = all_closes$Row.names
      all_closes$Row.names = NULL
    }
  }
  all_closes = get.between.dates(all_closes, start.date, end.date)
  return(all_closes)
}

stock.beta <- function(syms, benchmark.stock = 'spy', start.date = '2019-03-25', end.date = Sys.Date()) {
  syms = c(benchmark.stock, syms)
  all_closes = stock.loads(syms, start.date, end.date, cache = TRUE)
  co = stock.corr.helper(all_closes)
  sv = stock.vol(all_closes[, 1])
  ns = length(syms)
  betas = c()
  vols = c()
  for (n in 1:ns) {
    # volitility
    val = stock.vol(all_closes[, n])
    vols = c(vols, val)
    betas = c(betas, co[1, n] * val / sv)
  }
  print(vols)
  return(betas)
}

main <- function(args = commandArgs(trailingOnly = TRUE))
{
  option_list = list(
      make_option(
          c("-s", "--symbols"),
          type = "character",
          help = "symbols seperated by comma(,)",
          default = "nugt,dust"
      ),
      make_option(
          c("--start"),
          type = "character",
          help = paste0("start date YYYY-mm-dd",
                 "start date ======"),
          default = "2018-01-01"
      )
  )
  opt = parse_args(OptionParser(usage = "usage: %prog [options]", 
                   option_list = option_list))

  cat(as.yaml(opt))
  syms = strsplit(opt$symbols, ",")[[1]]

  print(opt$start)
  sc = stock.corr(c("spy", syms), start = opt$start, cache = TRUE)
  print(sc)
  betas = stock.beta(syms, start = opt$start)
  betas = data.frame(betas)
  row.names(betas) = c("spy", syms)
  colnames(betas) = c("beta")
  print(betas)
}
