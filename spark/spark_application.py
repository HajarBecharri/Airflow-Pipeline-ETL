from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os
import shutil

# Initialize Spark session
spark = SparkSession.builder \
    .appName("DataTransformationForAnalysis") \
    .getOrCreate()

# Load data
file_path = "/home/hajar/airflow/data/train.csv"
df = spark.read.csv(file_path, header=True, inferSchema=True)

# 1. Select only the required columns
columns_to_keep = [
    'Age', 'Attrition', 'BusinessTravel', 'Department',
    'Education', 'EducationField', 'Gender', 'JobSatisfaction',
    'MonthlyIncome', 'NumCompaniesWorked', 'PercentSalaryHike',
    'PerformanceRating', 'RelationshipSatisfaction', 'TotalWorkingYears',
    'TrainingTimesLastYear', 'YearsAtCompany', 'YearsInCurrentRole', 'YearsWithCurrManager'
]
df = df.select(columns_to_keep)

# 2. Handle missing values
# Fill missing numeric values with median
numeric_columns = [col for col, dtype in df.dtypes if dtype in ('int', 'double')]
for column in numeric_columns:
    median_value = df.approxQuantile(column, [0.5], 0.0)[0]
    df = df.na.fill({column: median_value})

# Fill missing categorical values with mode
categorical_columns = [col for col, dtype in df.dtypes if dtype == 'string']
for column in categorical_columns:
    mode_value = df.groupBy(column).count().orderBy("count", ascending=False).first()[0]
    df = df.na.fill({column: mode_value})

# 3. Optional: Create derived columns for analysis
# Example: Calculate years since joining
df = df.withColumn(
    "YearsSinceJoin", col("Age") - col("TotalWorkingYears") - col("YearsAtCompany")
)

# 4. Display transformed data for verification
df.show(5, truncate=False)

# 5. Save transformed data
output_path = "/home/hajar/airflow/data/transformed_train.csv"
# Réduire à une seule partition et écrire le fichier CSV
df.coalesce(1).write.option("header", "true").csv(output_path)
# Spécifier le nouveau nom du fichier
new_file_name = "/home/hajar/airflow/data/fixed_transformed_train.csv"

# Renommer et déplacer le fichier généré
for file in os.listdir(output_path):
    if file.startswith("part-00000"):
        shutil.move(os.path.join(output_path, file), new_file_name)

# Stop Spark session
spark.stop()
