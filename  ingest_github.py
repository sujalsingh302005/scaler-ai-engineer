import os
import shutil
from git import Repo

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

REPOS = [
    "https://github.com/sujalsingh302005/AI-Mock-Interviewer.git",
]

if os.path.exists("repos"):
    shutil.rmtree("repos")

os.makedirs("repos")

all_text = ""

for repo_url in REPOS:

    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = f"repos/{repo_name}"

    print(f"Cloning {repo_name}...")

    Repo.clone_from(repo_url, repo_path)

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [
            d for d in dirs
            if d not in [".git", "node_modules", ".next", "venv"]
        ]

        for file in files:

            if file.endswith((
                ".py",
                ".js",
                ".jsx",
                ".ts",
                ".tsx",
                ".md",
                ".txt"
            )):

                path = os.path.join(root, file)

                try:
                    with open(
                        path,
                        "r",
                        encoding="utf-8",
                        errors="ignore"
                    ) as f:

                        content = f.read()

                        all_text += f"\n\nFILE: {path}\n"
                        all_text += content

                except:
                    pass

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.create_documents([all_text])

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="./db",
    embedding_function=embeddings
)

db.add_documents(chunks)

print("GitHub repositories indexed successfully!")