library('derivmkts')

f <- file("stdin")
open(f)
while(length(line <- readLines(f,n=1)) > 0) {
  write(line, stderr())
  # process line
}

greeks(bscall(s=170, k=180, v=0.10, r=0.035, tt=120/365, d=0))



