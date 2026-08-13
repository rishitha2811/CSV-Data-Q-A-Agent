import sys
import os
from dotenv import load_dotenv

load_dotenv()

from agent.engine import DataQAAgent

def main():
    # Automatically use the sample dataset inside data/sales_data.csv
    csv_path = os.path.join("data", "sales_data.csv")
    
    # If the user provided a custom CSV file path in command line, use that instead
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        csv_path = sys.argv[1]
    print("\n" + "="*60)
    print("🤖 DATA Q&A AI AGENT - INTERACTIVE CHAT")
    print("="*60)
    print(f"📁 Loaded Dataset: {csv_path}")
    print("💡 Type your question below (or type 'exit' or 'quit' to stop).\n")

    try:
        agent = DataQAAgent(csv_path=csv_path)
    except Exception as e:
        print(f"❌ Initialization Error: {e}")
        sys.exit(1)

    # Interactive Chat Loop
    while True:
        try:
            # Wait for user to type a question
            user_question = input("\n💬 You: ").strip()
            
            # Check if user wants to stop
            if user_question.lower() in ["exit", "quit", "q"]:
                print("\n👋 Goodbye! Agent session closed.\n")
                break
                
            if not user_question:
                continue

            print("\n🤔 Agent is analyzing and calculating...")
            
            # Ask the agent
            output = agent.ask(user_question)

            print("\n" + "-"*40)
            print("🐍 Executed Code:")
            print(output["code"])
            print("-"*40)
            print("📊 Computed Result:")
            print(output["raw_result"])
            print("-"*40)
            print("🤖 Final Answer:")
            print(output["answer"])
            print("-"*40)

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Agent session closed.\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()