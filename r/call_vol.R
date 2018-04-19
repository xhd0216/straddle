library('derivmkts')

f <- file("stdin")
open(f)
while(length(line <- readLines(f, n=1)) > 0) {
  arr <- strsplit(line, "\\s+")
  print(bscallimpvol(s=as.double(arr[[1]][1]), k=as.double(arr[[1]][2]), r=as.double(arr[[1]][3]), tt=as.double(arr[[1]][4]), d=0, price=as.double(arr[[1]][5])))
  #write(' ', stdout())
}
