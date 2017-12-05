library(ggplot2)

interest_tracks <- read.csv('tracks.txt')
summary(interest_tracks)

interest_tracks$duration <- interest_tracks$end - interest_tracks$begin
interest_tracks$norm_word_positon <- interest_tracks$word_position / interest_tracks$word_num_phones
interest_tracks$norm_time <- (interest_tracks$time - interest_tracks$begin) / interest_tracks$duration
interest_tracks$utt_norm_time <- interest_tracks$norm_time + interest_tracks$utterance_position
interest_tracks$element_norm_time <- (interest_tracks$norm_time * interest_tracks$norm_word_positon) + interest_tracks$word_element_number
interest_tracks$phone_id <- paste(interest_tracks$phone, interest_tracks$discourse, as.character(interest_tracks$begin),sep='_')
interest_tracks <- merge(interest_tracks, condition.data)

interest_tracks[interest_tracks$Focus == 'Wide',]$element_norm_time <- interest_tracks[interest_tracks$Focus == 'Wide',]$element_norm_time + 2


t_data = subset(interest_tracks, element_norm_time >= 4)
summary(t_data)
ggplot(aes(x=element_norm_time, y = F0_relative), data= t_data) + geom_smooth() + facet_grid(Focus~Structure*Intonation) + scale_x_continuous(breaks=seq(1:7))
ggsave('utt_pitch_tracks.pdf', width = 8, height = 8)
