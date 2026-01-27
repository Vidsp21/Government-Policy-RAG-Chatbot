from query.retriever import retrieve_context
from query.rag_chain import generate_answer

def main():
    question = input("Ask a government policy question: ")

    docs = retrieve_context(question)
    context = "\n\n".join([doc.page_content for doc in docs])

    answer = generate_answer(context, question)

    print("\nAnswer:\n")
    print(answer)

if __name__ == "__main__":
    main()
