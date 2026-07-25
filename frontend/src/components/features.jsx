export const predictionFeatures = [
  "Login_Frequency",
  "Average_Session_Duration_Min",
  "Video_Completion_Rate",
  "Discussion_Participation",
  "Time_Spent_Hours",
  "Days_Since_Last_Login",
  "Notifications_Checked",
  "Peer_Interaction_Score",
  "Assignments_Submitted",
  "Assignments_Missed",
  "Quiz_Attempts",
  "Quiz_Score_Avg",
  "Project_Grade",
  "Progress_Percentage",
  "Rewatch_Count",
  "App_Usage_Percentage",
  "Reminder_Emails_Clicked",
];

export const clusterFeatures = predictionFeatures;



export const randomStudent = {

  Login_Frequency:
    Math.floor(Math.random() * 20) + 10,

  Average_Session_Duration_Min:
    Math.floor(Math.random() * 60) + 20,

  Video_Completion_Rate:
    Math.floor(Math.random() * 40) + 60,

  Discussion_Participation:
    Math.floor(Math.random() * 10) + 1,

  Time_Spent_Hours:
    Math.floor(Math.random() * 40) + 10,

  Days_Since_Last_Login:
    Math.floor(Math.random() * 10) + 1,

  Notifications_Checked:
    Math.floor(Math.random() * 20) + 5,

  Peer_Interaction_Score:
    Math.floor(Math.random() * 50) + 50,

  Assignments_Submitted:
    Math.floor(Math.random() * 10) + 5,

  Assignments_Missed:
    Math.floor(Math.random() * 3),

  Quiz_Attempts:
    Math.floor(Math.random() * 10) + 1,

  Quiz_Score_Avg:
    Math.floor(Math.random() * 30) + 70,

  Project_Grade:
    Math.floor(Math.random() * 30) + 70,

  Progress_Percentage:
    Math.floor(Math.random() * 30) + 70,

  Rewatch_Count:
    Math.floor(Math.random() * 10),

  App_Usage_Percentage:
    Math.floor(Math.random() * 30) + 70,

  Reminder_Emails_Clicked:
    Math.floor(Math.random() * 10) + 1

};

