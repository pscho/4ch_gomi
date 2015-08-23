# mean time_difference in order from oldest to newest thread:

# [1] 314.5425 5 posts
# [1] 304.5504 23 posts
# [1] 365.4917 12 posts (most words?)
# [1] 505.898 0 posts
# [1] 295.72 0 posts

library(ggplot2)
df = read.csv("G:/pentasori/Documents/Visual Studio 2015/Projects/cl_jobs/cl_jobs/posts.csv")
d <- ggplot(df, aes(x=seq_along(time_difference), y=time_difference) )
user <- which(df$user_post %in% "True")

d + geom_point(color=ifelse(df$user_post=="True", 'red', 'black')) + geom_line()

max(df$time_difference) / 60
mean(df$time_difference)
df$post_num[which(df$time_difference %in% max(df$time_difference))]

