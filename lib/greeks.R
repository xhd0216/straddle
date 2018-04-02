library('derivmkts')

f <- file("stdin")
open(f)
while(length(line <- readLines(f, n=1)) > 0) {
  arr <- strsplit(line, "\\s+")
  print(greeks(bscall(s=as.double(arr[[1]][1]), k=as.double(arr[[1]][2]), v=as.double(arr[[1]][3]), r=as.double(arr[[1]][4]), tt=as.double(arr[[1]][5]), d=0)))
  #print(greeks(bscall(s=170, k=180, v=0.10, r=0.035, tt=120/365, d=0)))
  write(' ', stdout())
}




