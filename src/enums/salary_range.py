from enum import Enum

class SalaryRange(Enum):
    Undisclosed = "Salary Range Unknown"
    AverageRange_30K = "Average Salary Range Below 30K"
    AverageRange_60K = "Average Salary Range 30K-59K"
    AverageRange_90K = "Average Salary Range 60K-89K"
    AverageRange_120K = "Average Salary Range 90K-119K"
    AverageRange_Above120K = "Average Salary Range At Least 120K"