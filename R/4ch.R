# mean time_difference in order from oldest to newest thread:

# [1] 314.5425 5 posts
# [1] 304.5504 23 posts
# [1] 365.4917 12 posts (most words?)
# [1] 505.898 0 posts
# [1] 340.9305 0 posts (adjusted for site downtime)

#######

library(ggplot2)

convertTime <- function(ts) {
  return(format(as.POSIXct(ts, origin="1970-01-01"),"%H")) # format: "%H:%M:%S"
}

## import
df = read.csv("G:/pentasori/Documents/Visual Studio 2015/Projects/cl_jobs/cl_jobs/output/combined.csv")

# remove largest outlier due to site downtime
df <- df[-which(df$time_difference %in% max(df$time_difference)),]

# convert unix timestamp into 24-hour time
df$time24 <- apply(data.frame(df[,"timestamp"]), 1, convertTime)

max(df$time_difference) / 60
mean(df$time_difference)
df$post_num[which(df$time_difference %in% max(df$time_difference))]

d <- ggplot(df, aes(x=time_difference, y=time24) )
d + geom_point(color=ifelse(df$user_post=="True", 'red', 'black'))

times <- c('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',
           '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23')
for (i in times) {
  print(i)
  print(mean(subset(df, df$time24==i)$time_difference))
}
