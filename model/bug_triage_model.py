import io
import os
import re
import zipfile

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# Common English stopwords - built-in fallback to avoid NLTK download
COMMON_STOPWORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 
    'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can', 
    "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 
    'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 
    'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 
    'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 
    'its', 'itself', 'just', 'k', 'me', "me're", 'might', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 
    'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 
    'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 
    'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', 
    "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', "shan't", 'until', 
    'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 
    'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'will', "won't", 
    'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 
    'yourselves'
}


def _repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BugTriageModel:
    def __init__(self):
        self.assignment_vectorizer = None
        self.priority_vectorizer = None
        self.classifier = None
        self.priority_classifier = None
        self.stop_words = COMMON_STOPWORDS

    def preprocess_text(self, text):
        """
        Preprocess the input text by:
        1. Converting to lowercase
        2. Removing special characters and numbers
        3. Tokenizing
        4. Removing stopwords
        """
        text = "" if pd.isna(text) else str(text)
        text = text.lower()
        text = re.sub(r"[^a-zA-Z\s]", " ", text)
        # Simple split tokenization instead of NLTK
        tokens = text.split()
        tokens = [word for word in tokens if word not in self.stop_words and len(word) > 0]
        return " ".join(tokens)

    def _canonicalize_frame(self, df, title_col, description_col, assigned_col=None, priority_col=None):
        canonical = pd.DataFrame(
            {
                "title": df[title_col].fillna("").astype(str),
                "description": df[description_col].fillna("").astype(str),
            }
        )

        if assigned_col:
            canonical["assigned_to"] = df[assigned_col].fillna("").astype(str)

        if priority_col:
            canonical["priority"] = df[priority_col].apply(self._normalize_priority_label)

        canonical["title"] = canonical["title"].str.strip()
        canonical["description"] = canonical["description"].str.strip()
        canonical = canonical[(canonical["title"] != "") | (canonical["description"] != "")]
        return canonical

    def _normalize_priority_label(self, value):
        if pd.isna(value):
            return None

        text = str(value).strip().lower()
        priority_map = {
            "p1": "high",
            "p2": "high",
            "p3": "medium",
            "p4": "low",
            "p5": "low",
            "blocker": "high",
            "critical": "high",
            "major": "medium",
            "normal": "medium",
            "minor": "low",
            "trivial": "low",
            "enhancement": "low",
            "high": "high",
            "medium": "medium",
            "low": "low",
            "1": "high",
            "0": "low",
        }
        return priority_map.get(text, text)

    def _build_processed_text(self, df):
        prepared = df.copy()
        prepared["combined_text"] = (
            prepared["title"].fillna("").astype(str) + " " + prepared["description"].fillna("").astype(str)
        ).str.strip()
        prepared["processed_text"] = prepared["combined_text"].apply(self.preprocess_text)
        return prepared[prepared["processed_text"].str.strip() != ""]

    def _fit_vectorizer(self, texts):
        vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
        return vectorizer, vectorizer.fit_transform(texts)

    def _load_repo_dataset(self):
        # Try to load enhanced dataset first, fall back to original
        enhanced_filepath = os.path.join(_repo_root(), "data", "enhanced_bug_reports.csv")
        original_filepath = os.path.join(_repo_root(), "data", "bug_reports.csv")

        if os.path.exists(enhanced_filepath):
            print(f"Loading enhanced dataset from {enhanced_filepath}")
            df = pd.read_csv(enhanced_filepath)
        elif os.path.exists(original_filepath):
            print(f"Loading original dataset from {original_filepath}")
            df = pd.read_csv(original_filepath)
        else:
            print("No dataset found!")
            return pd.DataFrame()

        return self._canonicalize_frame(
            df,
            title_col="title",
            description_col="description",
            assigned_col="assigned_to",
            priority_col="priority",
        )

    def _load_sample_dataset(self, filepath):
        if not filepath or not os.path.exists(filepath):
            return pd.DataFrame(columns=["title", "description", "assigned_to", "priority"])

        df = pd.read_csv(filepath)
        return self._canonicalize_frame(
            df,
            title_col="Summary",
            description_col="Description",
            assigned_col="Assigned to",
            priority_col="Priority",
        )

    def _load_archive_priority_dataset(self, zip_path):
        if not zip_path or not os.path.exists(zip_path):
            return pd.DataFrame(columns=["title", "description", "priority"])

        frames = []
        with zipfile.ZipFile(zip_path) as archive:
            for member in ("sev_train.csv", "sev_test.csv", "sev.csv"):
                if member not in archive.namelist():
                    continue

                with archive.open(member) as handle:
                    df = pd.read_csv(io.BytesIO(handle.read()))

                normalized = pd.DataFrame(
                    {
                        "title": df["Description"].fillna("").astype(str).str.slice(0, 120),
                        "description": df["Description"].fillna("").astype(str),
                        "priority": df["Label"].apply(self._normalize_priority_label),
                    }
                )
                frames.append(normalized)

        if not frames:
            return pd.DataFrame(columns=["title", "description", "priority"])

        return pd.concat(frames, ignore_index=True).drop_duplicates(subset=["title", "description", "priority"])

    def build_training_frames(self, sample_csv_path=None, archive_zip_path=None):
        repo_df = self._load_repo_dataset()
        sample_df = self._load_sample_dataset(sample_csv_path)
        archive_priority_df = self._load_archive_priority_dataset(archive_zip_path)

        assignment_df = pd.concat(
            [repo_df[["title", "description", "assigned_to"]], sample_df[["title", "description", "assigned_to"]]],
            ignore_index=True,
        )
        assignment_df = assignment_df.dropna(subset=["assigned_to"])
        assignment_df = assignment_df[assignment_df["assigned_to"].str.strip() != ""]
        assignment_df = assignment_df.drop_duplicates()

        priority_sources = [repo_df[["title", "description", "priority"]]]
        if not sample_df.empty:
            priority_sources.append(sample_df[["title", "description", "priority"]])
        if not archive_priority_df.empty:
            priority_sources.append(archive_priority_df[["title", "description", "priority"]])

        priority_df = pd.concat(priority_sources, ignore_index=True)
        priority_df = priority_df.dropna(subset=["priority"])
        priority_df = priority_df[priority_df["priority"].str.strip() != ""]
        priority_df = priority_df.drop_duplicates()

        return assignment_df, priority_df

    def train_from_frames(self, assignment_df, priority_df):
        assignment_prepared = self._build_processed_text(assignment_df)
        priority_prepared = self._build_processed_text(priority_df)

        self.assignment_vectorizer, X_assignment = self._fit_vectorizer(assignment_prepared["processed_text"])
        self.priority_vectorizer, X_priority = self._fit_vectorizer(priority_prepared["processed_text"])

        y_assigned = assignment_prepared["assigned_to"]
        y_priority = priority_prepared["priority"]

        X_assign_train, X_assign_test, y_assign_train, y_assign_test = train_test_split(
            X_assignment, y_assigned, test_size=0.2, random_state=42
        )
        X_priority_train, X_priority_test, y_priority_train, y_priority_test = train_test_split(
            X_priority, y_priority, test_size=0.2, random_state=42
        )

        self.classifier = MultinomialNB()
        self.classifier.fit(X_assign_train, y_assign_train)

        self.priority_classifier = LogisticRegression(random_state=42, max_iter=1000)
        self.priority_classifier.fit(X_priority_train, y_priority_train)

        assign_pred = self.classifier.predict(X_assign_test)
        priority_pred = self.priority_classifier.predict(X_priority_test)

        print(f"Assignment training rows: {len(assignment_prepared)}")
        print("Assignment Model Evaluation:")
        print(f"Accuracy: {accuracy_score(y_assign_test, assign_pred):.4f}")
        print(f"Precision: {precision_score(y_assign_test, assign_pred, average='weighted', zero_division=0):.4f}")
        print(f"Recall: {recall_score(y_assign_test, assign_pred, average='weighted', zero_division=0):.4f}")
        print(f"F1-Score: {f1_score(y_assign_test, assign_pred, average='weighted', zero_division=0):.4f}")

        print(f"\nPriority training rows: {len(priority_prepared)}")
        print("Priority Model Evaluation:")
        print(f"Accuracy: {accuracy_score(y_priority_test, priority_pred):.4f}")
        print(f"Precision: {precision_score(y_priority_test, priority_pred, average='weighted', zero_division=0):.4f}")
        print(f"Recall: {recall_score(y_priority_test, priority_pred, average='weighted', zero_division=0):.4f}")
        print(f"F1-Score: {f1_score(y_priority_test, priority_pred, average='weighted', zero_division=0):.4f}")

    def predict(self, title, description):
        """
        Predict the assigned team and priority for a new bug report.
        """
        combined_text = f"{title} {description}".strip()
        processed_text = self.preprocess_text(combined_text)

        assignment_X = self.assignment_vectorizer.transform([processed_text])
        priority_X = self.priority_vectorizer.transform([processed_text])

        assign_pred = self.classifier.predict(assignment_X)[0]
        assign_proba = self.classifier.predict_proba(assignment_X)[0]
        assign_confidence = float(max(assign_proba))

        priority_pred = self.priority_classifier.predict(priority_X)[0]
        priority_proba = self.priority_classifier.predict_proba(priority_X)[0]
        priority_confidence = float(max(priority_proba))

        return {
            "assigned_to": str(assign_pred),
            "assignment_confidence": assign_confidence,
            "priority": str(priority_pred),
            "priority_confidence": priority_confidence,
        }

    def save_model(self, filepath):
        """
        Save the trained model to disk.
        """
        model_data = {
            "assignment_vectorizer": self.assignment_vectorizer,
            "priority_vectorizer": self.priority_vectorizer,
            "classifier": self.classifier,
            "priority_classifier": self.priority_classifier,
        }
        joblib.dump(model_data, filepath)

    def load_model(self, filepath):
        """
        Load a trained model from disk.
        """
        model_data = joblib.load(filepath)
        self.assignment_vectorizer = model_data.get("assignment_vectorizer") or model_data.get("vectorizer")
        self.priority_vectorizer = model_data.get("priority_vectorizer") or model_data.get("vectorizer")
        self.classifier = model_data["classifier"]
        self.priority_classifier = model_data["priority_classifier"]

    def detect_duplicates(self, new_title, new_description, existing_reports, threshold=0.8):
        """
        Detect potential duplicate bug reports using cosine similarity.
        """
        if existing_reports.empty:
            return []

        new_combined = f"{new_title} {new_description}".strip()
        new_processed = self.preprocess_text(new_combined)
        vectorizer = self.assignment_vectorizer or self.priority_vectorizer
        new_vector = vectorizer.transform([new_processed])

        duplicates = []
        for _, report in existing_reports.iterrows():
            existing_combined = f"{report['title']} {report['description']}".strip()
            existing_processed = self.preprocess_text(existing_combined)
            existing_vector = vectorizer.transform([existing_processed])
            similarity = (new_vector * existing_vector.T).toarray()[0][0]
            report_id = report["id"] if "id" in report.index else report.name

            if similarity >= threshold:
                duplicates.append(
                    {
                        "id": int(report_id),
                        "title": report["title"],
                        "similarity": float(similarity),
                    }
                )

        return duplicates


if __name__ == "__main__":
    model = BugTriageModel()

    sample_csv_path = os.path.expanduser(r"~/Downloads/sample_data.csv")
    archive_zip_path = os.path.expanduser(r"~/Downloads/archive.zip")

    assignment_df, priority_df = model.build_training_frames(
        sample_csv_path=sample_csv_path,
        archive_zip_path=archive_zip_path,
    )
    model.train_from_frames(assignment_df, priority_df)
    model.save_model(os.path.join(_repo_root(), "model", "bug_triage_model.pkl"))

    print("Model trained and saved successfully!")
