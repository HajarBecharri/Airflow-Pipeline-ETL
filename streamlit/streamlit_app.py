import psycopg2
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Connexion à la base de données PostgreSQL
conn = psycopg2.connect(
    dbname="airflow_db", 
    user="postgres", 
    password="12345", 
    host="localhost", 
    port="5432"
)

# Charger les données dans un DataFrame Pandas
query = "SELECT * FROM employee_data"  # Remplacez par le nom de votre table
df = pd.read_sql(query, conn)
conn.close()

# Options de filtrage dans Streamlit
st.sidebar.title("Filtres")

# Filtres pour Education
education_filter = st.sidebar.multiselect("Education", options=df['education'].unique(), default=df['education'].unique())
# Filtres pour Department
department_filter = st.sidebar.multiselect("Department", options=df['department'].unique(), default=df['department'].unique())

# Appliquer les filtres
filtered_data = df[(df['education'].isin(education_filter)) & (df['department'].isin(department_filter))]

# Affichage du tableau de bord
st.title("Tableau de Bord d'Analyse des Données Employés")

# Afficher les données filtrées
st.subheader("Données Filtrées")
st.write(filtered_data.head())

# Graphiques interactifs avec filtrage
# 1. Revenu Mensuel par Genre et Département
st.subheader("Revenu Mensuel par Genre et Département")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=filtered_data, x='gender', y='monthlyincome', hue='department', estimator='mean', ci=None, palette='pastel', ax=ax)
ax.set_xlabel('Genre')
ax.set_ylabel('Revenu Mensuel Moyen')
st.pyplot(fig)
# 1. Revenu Mensuel par Âge
st.subheader("Relation entre Revenu Mensuel et Âge")
fig, ax = plt.subplots()
sns.lineplot(data=filtered_data, x='age', y='monthlyincome', ax=ax, marker='o', color='b')
ax.set_xlabel('Âge')
ax.set_ylabel('Revenu Mensuel')
st.pyplot(fig)

# 2. Revenu Mensuel par Genre
st.subheader("Revenu Mensuel par Genre")
fig, ax = plt.subplots()
sns.barplot(data=filtered_data, x='gender', y='monthlyincome', estimator='mean', ci=None, palette='pastel', ax=ax)
ax.set_xlabel('Genre')
ax.set_ylabel('Revenu Mensuel Moyen')
st.pyplot(fig)

# 4. Relation entre Revenu Mensuel et Total d'Années de Travail
st.subheader("Relation entre Revenu Mensuel et Total d'Années de Travail")
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_data, x='totalworkingyears', y='monthlyincome', hue='gender', palette='cool', ax=ax)
ax.set_xlabel("Total d'Années de Travail")
ax.set_ylabel('Revenu Mensuel')
st.pyplot(fig)

# 5. Revenu Mensuel par Niveau d'Éducation
st.subheader("Revenu Mensuel Moyen par Niveau d'Éducation")
fig, ax = plt.subplots()
sns.barplot(data=filtered_data, x='education', y='monthlyincome', estimator='mean', ci=None, palette='viridis', ax=ax)
ax.set_xlabel("Niveau d'Éducation")
ax.set_ylabel('Revenu Mensuel Moyen')
st.pyplot(fig)

# 6. Revenu Mensuel par Département
st.subheader("Revenu Mensuel Moyen par Département")
fig, ax = plt.subplots()
sns.barplot(data=filtered_data, x='department', y='monthlyincome', estimator='mean', ci=None, palette='magma', ax=ax)
ax.set_xlabel("Département")
ax.set_ylabel('Revenu Mensuel Moyen')
st.pyplot(fig)

# Relation entre Revenu Mensuel et Années avec le Manager Actuel
st.subheader("Revenu Mensuel en fonction des Années avec le Manager Actuel")
fig, ax = plt.subplots()
sns.lineplot(data=filtered_data, x='yearswithcurrmanager', y='monthlyincome', marker='o', color='teal', ax=ax)
ax.set_xlabel("Années avec le Manager Actuel")
ax.set_ylabel('Revenu Mensuel')
st.pyplot(fig)

# Fermez tous les graphiques pour éviter les conflits
plt.close('all')
