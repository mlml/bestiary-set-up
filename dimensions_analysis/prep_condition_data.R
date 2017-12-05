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
