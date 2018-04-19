library('tseries')

args <- commandArgs(trailingOnly = TRUE)

a <- get.hist.quote(args[1], start=args[2], end=args[3])

sink(paste(args[1], "-", args[2], "-", args[3], ".csv", sep=""))

a
