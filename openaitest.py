import cohere

co = cohere.ClientV2(api_key="Eit2CbBUqoP0pQStDSxDwAYPcTomoMNEZAuAmLLn")

res = co.chat(
    model="command-a-03-2025",
    messages=[
        {
            "role": "user",
            "content": "write a email to boss for leave",
        }
    ],
)

print(res.message.content[0].text)
# print(res)

# "The Ultimate Guide to API Design: Best Practices for Building Robust and Scalable APIs"
