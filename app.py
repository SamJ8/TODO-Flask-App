from website import create_app
app = create_app()

if __name__=="__main__":
    
    app.run(debug=True, port=8000)

    #! This is where the actual running of the app occurs.
    #! When running the app, app = create_app() will create all the tables we need in the database.