from tasks import research_task, write_task, proof_read_task

def main():
    topic = "Artificial Intelligence in Finance"
    
    # Step 1: Research
    print(">>> Running Research Task")
    research_output = research_task(topic)
    print("Research Output:")
    print(research_output)
    
    # Step 2: Writing
    print("\n>>> Running Writing Task")
    article_output = write_task(topic, research_output)
    print("Article Output:")
    print(article_output)
    
    # Step 3: Proofreading
    print("\n>>> Running Proofreading Task")
    final_output = proof_read_task(topic, article_output)
    print("\nFinal Newsletter:")
    print(final_output)

if __name__ == "__main__":
    main()
