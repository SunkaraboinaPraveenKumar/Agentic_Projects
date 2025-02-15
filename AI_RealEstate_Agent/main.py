from tasks import research_task, write_task

def main():
    topic = "Hyderabad City Real Estate Market"
    
    # Step 1: Research
    print(">>> Running Research Task")
    research_output = research_task(topic)
    print("Research Output:")
    print(research_output)
    
    # Save the research data to a text file
    with open("research_data.txt", "w") as f:
        f.write(research_output)
    
    # Step 2: Writing/Analysis
    print("\n>>> Running Writing Task")
    article_output = write_task(topic, research_output)
    print("Article Output:")
    print(article_output)

if __name__ == "__main__":
    main()
