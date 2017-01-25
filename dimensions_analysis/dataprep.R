library(ggplot2)
library(dplyr)
library(stringr)

# Get condition information

suborn <- read.delim('C:/Users/michael/Dropbox/dimensions/suborn_responses.txt')
suborn$discourse <- str_replace(suborn$recordedFile, '.wav', '')
suborn$Focus <- factor(suborn$condition, labels = c('Third','Second','First','Wide'))
suborn$Intonation <- 'Declarative'
suborn$Structure <- factor(suborn$bracketing, labels =c("(AB)C", "A(BC)"))

suborn <- suborn[,c('discourse', 'Focus', 'Intonation', 'Structure')]

suborq <- read.delim('C:/Users/michael/Dropbox/dimensions/suborq_responses.txt')
suborq$discourse <- str_replace(suborq$recordedFile, '.wav', '')
suborq$Focus <- factor(suborq$bracketing, labels = c('Third','Second','First','Wide'))
suborq$Intonation <- 'Interrogative'
suborq$Structure <- factor(suborq$order, labels =c("(AB)C", "A(BC)"))

suborq <- suborq[,c('discourse', 'Focus', 'Intonation', 'Structure')]

condition.data <- rbind(suborn, suborq)

t <- read.csv('C:/Users/michael/Dropbox/dimensions/pgdb_analysis.txt')

t$Constituent <- factor(t$element_number, labels = c('A', 'B', 'C'))

t <- merge(t, condition.data)
t$Intonation <- factor(t$Intonation)

t <- na.omit(t) # Whole word creaky

t$Focus <- factor(t$Focus, levels = c('Wide', 'First', 'Second','Third'))

ggplot(aes(x=Constituent, y=Mean_F0), data=t) + stat_summary(fun.data="mean_cl_boot") + stat_summary(fun.y=mean, geom="line", aes(group=interaction(Focus,Intonation,Structure))) + facet_grid(Focus~Structure*Intonation) + ylab('Mean F0')
ggsave('raw_F0.pdf', width = 8, height = 8)

ggplot(aes(x=Constituent, y=Mean_F0_relative), data=t) + stat_summary(fun.data="mean_cl_boot") + stat_summary(fun.y=mean, geom="line", aes(group=interaction(Focus,Intonation,Structure))) + facet_grid(Focus~Structure*Intonation) + ylab('Mean relative F0')
ggsave('relative_F0.pdf', width = 8, height = 8)

ggplot(aes(x=Constituent, y=duration), data=t) + stat_summary(fun.data="mean_cl_boot")  + stat_summary(fun.y=mean, geom="line", aes(group=interaction(Focus,Intonation,Structure))) + facet_grid(Focus~Structure*Intonation) + ylab('Mean duration')
ggsave('raw_duration.pdf', width = 8, height = 8)

ggplot(aes(x=Constituent, y=relative_duration), data=t) + stat_summary(fun.data="mean_cl_boot")  + stat_summary(fun.y=mean, geom="line", aes(group=interaction(Focus,Intonation,Structure))) + facet_grid(Focus~Structure*Intonation) + ylab('Mean relative duration')
ggsave('relative_duration.pdf', width = 8, height = 8)

ggplot(aes(x=Constituent, y=Mean_Intensity), data=t) + stat_summary(fun.data="mean_cl_boot")  + stat_summary(fun.y=mean, geom="line", aes(group=interaction(Focus,Intonation,Structure))) + facet_grid(Focus~Structure*Intonation) + ylab('Mean Intensity')
ggsave('raw_intensity.pdf', width = 8, height = 8)

ggplot(aes(x=Constituent, y=Mean_Intensity_relative), data=t) + stat_summary(fun.data="mean_cl_boot")  + stat_summary(fun.y=mean, geom="line", aes(group=interaction(Focus,Intonation,Structure))) + facet_grid(Focus~Structure*Intonation) + ylab('Mean relative Intensity')
ggsave('relative_intensity.pdf', width = 8, height = 8)
