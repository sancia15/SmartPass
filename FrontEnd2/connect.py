from flask import Flask, render_template, request, url_for

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("class.html")


@app.route("/", methods=["GET", "POST"])
def get_data():
    if request.method == "POST":
        X_pass = request.form["password"]
        import pandas as pd
        from password_strength import PasswordStats
        dataset = pd.read_csv(r"exp.txt")
        X = dataset.iloc[:, 1].values
        y = dataset.iloc[:, 3].values
        stats = PasswordStats(X_pass)
        X_test = [[stats.strength()]]

        # Splitting the data set into Training and Test set
        X_train = X.reshape(-1, 1)
        y_train = y.ravel()

        # Feature Scaling
        from sklearn.preprocessing import StandardScaler
        sc_X = StandardScaler()
        X_train = sc_X.fit_transform(X_train)
        X_test = sc_X.transform(X_test)

        # Fitting the simple linear regression to the training set
        from sklearn.linear_model import LogisticRegression
        classifier = LogisticRegression(random_state=0)
        classifier.fit(X_train, y_train)

        # Predicting Test Set Results
        y_pred = classifier.predict(X_test)
        f = y_pred[0]
        if f == 1:
            output = " breached category try another password"

        else:

            output = " Unbreached category go with it"
        return render_template('class.html', prediction_text='Your Password belongs to{}'.format(output))


if __name__ == '__main__':
    app.run(debug=True)
