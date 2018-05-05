library('derivmkts')

f <- file("stdin")
open(f)
while(length(line <- readLines(f, n=1)) > 0) {
  arr <- strsplit(line, "\\s+")
  s <- as.double(arr[[1]][1])
  k <- as.double(arr[[1]][2])
  r <- as.double(arr[[1]][3])
  tt <- as.double(arr[[1]][4])
  d <- 0
  price <- as.double(arr[[1]][5])
  tryCatch({
            iv <- bscallimpvol(s, k, r, tt, d, price)
            gr <- greeks(bscall(s, k, iv, r, tt, d))
            cat(c(iv, gr[2], gr[3], gr[4], gr[5], gr[6]), '\n')
            #     impvol, delta, gamma, vega, rho, theta
         },
         error=function(e){ NA },
         warning=function(w) { NA })
  #write(' ', stdout())
}
