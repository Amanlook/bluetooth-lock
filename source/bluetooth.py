import openai
from PIL import Image, ImageDraw, ImageFont
import textwrap
from datetime import datetime


openai.api_key = OPENAI_API_KEY
openai.base_url = OPENAI_BASE_URL



# Simple chat function
def chat(message: str, model: str = "gpt-4o", system_message: str = "You are a helpful assistant."):
    """
    Send a message to the chat model and get a response.
    
    Args:
        message: The user's message
        model: The model to use (e.g., gpt-4o, gpt-4, gpt-3.5-turbo)
        system_message: The system message to set the assistant's behavior
    
    Returns:
        The assistant's response text
    """
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in chat: {e}")
        return None




def create_funny_social_media_image(joke_text: str, output_filename: str = None):
    """
    Create a funny, social media-ready image with a joke.
    
    Args:
        joke_text: The joke text to display
        output_filename: Name for the output file (auto-generated if None)
    
    Returns:
        Path to the saved image
    """
    # Social media optimal size (Instagram post - 1080x1080)
    width, height = 1080, 1080
    
    # Create image with modern gradient background
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    
    # Create smooth gradient (vibrant purple to blue)
    for i in range(height):
        ratio = i / height
        # Smooth color transition
        r = int(138 - ratio * 70)  # 138 -> 68
        g = int(43 + ratio * 90)   # 43 -> 133
        b = int(226 - ratio * 24)  # 226 -> 202
        draw.rectangle([(0, i), (width, i + 1)], fill=(r, g, b))
    
    # Load fonts
    try:
        # Try common macOS fonts
        title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 70)
        text_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 50)
        small_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 35)
    except:
        try:
            # Fallback to Helvetica
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 70)
            text_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 50)
            small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 35)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
    
    # Add emoji at top
    emoji = "😂"
    draw.text((540, 150), emoji, fill="white", font=title_font, anchor="mm")
    
    # Draw white rounded rectangle for joke text
    rect_margin = 80
    rect_top = 380
    rect_bottom = 780
    rect_radius = 30
    
    # Draw single clean rounded rectangle
    draw.rounded_rectangle(
        [rect_margin, rect_top, width - rect_margin, rect_bottom],
        radius=rect_radius,
        fill=(255, 255, 255, 250)
    )
    
    # Add title above the box
    title = "DAILY JOKE"
    draw.text((540, 320), title, fill="white", font=title_font, anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0, 100))
    
    # Wrap and center joke text
    max_chars = 32
    wrapped_lines = textwrap.wrap(joke_text, width=max_chars)
    
    # Calculate total text height for vertical centering
    total_text_height = len(wrapped_lines) * 65
    y_start = rect_top + (rect_bottom - rect_top - total_text_height) // 2
    
    # Draw joke text (dark color on white background)
    for line in wrapped_lines:
        draw.text((540, y_start), line, fill="#1a1a1a", font=text_font, anchor="mm")
        y_start += 65
    
    # Add decorative bottom section
    draw.text((540, 860), "━━━━━━━", fill="white", font=small_font, anchor="mm")
    draw.text((540, 930), "Share & Spread Joy!", fill="white", font=small_font, anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0, 50))
    
    # Add small branding
    date_str = datetime.now().strftime("%B %d, %Y")
    draw.text((540, 1000), date_str, fill="white", font=small_font, anchor="mm")
    
    # Generate filename if not provided
    if output_filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"funny_joke_{timestamp}.png"
    
    # Save image
    img.save(output_filename, quality=95, optimize=True)
    print(f"✅ Social media image saved: {output_filename}")
    return output_filename


# Example usage
if __name__ == "__main__":
    # Get a funny joke from AI
    user_input = "Give me a short, funny joke in English (maximum 3-4 lines). Make it clean and suitable for social media."
    response = chat(user_input)
    
    if response:
        print(f"\n🎭 Generated Joke:\n{response}\n")
        # Create social media image
        image_path = create_funny_social_media_image(response)
        print(f"\n📸 Ready to share on Instagram, Facebook, Twitter!")
    else:
        print("Failed to generate joke")