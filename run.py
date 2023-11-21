from src import create_app

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        "db":db,
        "Members": Member
    }
    
if __name__ == '__main__':
    app.run()
