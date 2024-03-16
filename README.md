## Process Diagram
```mermaid
graph TD;
    A([Start]) --> B;
    B[User selects scripture verse from client dropdown] --> C;
    C["Create prompt with verse content with some padding and the verse name (i.e. Matthew 3:16)"] --> D;
    D["Prompt OpenAI GPT3.5"] --> E;
    E["LLM response is MidJourney prompt"] --> F;
    F["Send MJ prompt to MJ"] --> G;
    G["Get image in response"] --> H;
    H["Display image"] --> I([Finish]);
    H --> B;