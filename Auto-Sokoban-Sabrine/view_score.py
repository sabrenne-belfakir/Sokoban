import sqlite3

def display_scores():
    conn = sqlite3.connect('sokoban_scores.json')
    c = conn.cursor()
    c.execute('SELECT * FROM scores ORDER BY player_name, moves, time')
    scores = c.fetchall()
    conn.close()

    print("Player | Moves | Time")
    print("---------------------")
    for score in scores:
        print(f"{score[1]:5} | {score[2]:5} | {score[3]:.2f}")

if __name__ == "__main__":
    display_scores()
