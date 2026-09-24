
from src.agents.agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
    rewrite_chain  
)

def run_research_pipeline(topic: str) -> dict:
    state = {}

    # Step 1: Search Agent
    print("\n" + "=" * 50)
    print("[bold cyan]Step 1 - Search agent is working...[/bold cyan]")
    print("=" * 50)

    search_agent = build_search_agent()
    search_prompt = (
        f"Find recent, reliable and detailed information about: {topic}. "
        f"Include relevant URLs. If the topic is in Vietnamese, prioritize Vietnamese sources."
    )
    search_result = search_agent.invoke({
        "messages": [("user", search_prompt)]
    })
    messages = search_result.get("messages", [])
    state["search_results"] = messages[-1].content if messages else "No search results found."
    print("\n[green]Search Results:[/green]\n", state["search_results"])

    # Step 2: Reader Agent
    print("\n" + "=" * 50)
    print("[bold cyan]Step 2 - Reader agent is scraping top resources...[/bold cyan]")
    print("=" * 50)

    reader_agent = build_reader_agent()
    reader_prompt = (
        f"Based on the following search results about '{topic}', "
        f"pick the most relevant URL and scrape it for deeper content.\n\n"
        f"Search Results:\n{state['search_results'][:2000]}"
    )
    reader_result = reader_agent.invoke({
        "messages": [("user", reader_prompt)]
    })
    reader_messages = reader_result.get("messages", [])
    state["scraped_content"] = reader_messages[-1].content if reader_messages else "No content scraped."
    print("\n[green]Scraped Content:[/green]\n", state["scraped_content"])

    # Step 3: Writer Chain
    print("\n" + "=" * 50)
    print("[bold cyan]Step 3 - Writer is drafting the report...[/bold cyan]")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS:\n{state.get('search_results', '')}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state.get('scraped_content', '')}"
    )
    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })
    print("\n[green]Draft Report:[/green]\n", state["report"])

    # Step 4: Critic Chain 
    print("\n" + "=" * 50)
    print("[bold cyan]Step 4 - Critic is reviewing the report...[/bold cyan]")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state.get("report", "")
    })
    print("\n[yellow]Critic Feedback:[/yellow]\n", state["feedback"])

    # Step 5: Rewrite Chain 
    print("\n" + "=" * 50)
    print("[bold cyan]Step 5 - Rewriter is polishing the final report...[/bold cyan]")
    print("=" * 50)

    state["final_report"] = rewrite_chain.invoke({
        "topic": topic,
        "report": state.get("report", ""),
        "feedback": state.get("feedback", "")
    })
    print("\n[bold green]Final Polished Report:[/bold green]\n", state["final_report"])

    return state