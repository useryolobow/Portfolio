import json
import random

def generate_general_json(filename, target_size_mb=1.1):
    # Data components for generating "general" conversational data
    triggers = [
        "How do you feel about {topic}?",
        "What is your take on {topic}?",
        "Can you explain {topic} to me?",
        "Why is {topic} so popular right now?",
        "Have you ever tried {activity} in {place}?",
        "What's the best way to start {activity}?",
        "Tell me a fascinating fact about {topic}.",
        "Do you think {topic} will change in the next decade?",
        "What are the pros and cons of {topic}?",
        "I'm thinking of visiting {place}, what should I do there?"
    ]
    
    topics = ["Artificial Intelligence", "Climate Change", "Ancient History", "Molecular Gastronomy", 
              "Quantum Physics", "Renewable Energy", "Space Exploration", "Impressionist Art", 
              "Digital Privacy", "Sustainable Fashion", "Jazz Music", "Backpacking", "Gardening"]
    
    activities = ["scuba diving", "oil painting", "learning Python", "rock climbing", "baking sourdough", 
                  "meditating", "playing chess", "photography", "urban exploration", "pottery"]
    
    places = ["Tokyo", "Iceland", "Patagonia", "New York City", "The Swiss Alps", "Kyoto", "Berlin", 
              "The Great Barrier Reef", "Marrakech", "New Zealand"]

    responses = [
        "I find it {adj} and {adj}.",
        "It's a {adj} experience that really makes you think about {topic}.",
        "Honestly, I think it's {adj} but sometimes {adj}.",
        "Most people find it {adj}, though I personally think it matters for {topic}.",
        "It's definitely {adj}! You should try it if you like {topic}.",
        "The most important part is {topic}, which can be {adj} for beginners.",
        "I've heard it's {adj}, especially when you are in {place}."
    ]
    
    adjectives = ["incredible", "challenging", "mysterious", "rewarding", "overwhelming", "beautiful", 
                  "fascinating", "thought-provoking", "complex", "accessible", "vibrant", "serene"]

    data = {}
    
    # Generate until we hit the target size
    while True:
        topic = random.choice(topics)
        place = random.choice(places)
        activity = random.choice(activities)
        
        # Build a Trigger
        trigger_template = random.choice(triggers)
        trigger = trigger_template.format(topic=topic, activity=activity, place=place)
        
        # Build multiple Responses for this trigger
        resps_for_trigger = {}
        for _ in range(random.randint(3, 8)):
            adj1 = random.choice(adjectives)
            adj2 = random.choice(adjectives)
            resp_template = random.choice(responses)
            response_text = resp_template.format(adj=adj1, topic=topic, place=place).replace("{adj}", adj2, 1)
            resps_for_trigger[response_text] = random.randint(1, 500)
        
        data[trigger] = resps_for_trigger
        
        # Approximate size check to stop
        if len(json.dumps(data)) > target_size_mb * 1024 * 1024:
            break
            
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

generate_general_json("massive_general_data.json")