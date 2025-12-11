import telebot
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from google import genai # لاستخدام نموذج Gemini
from google.genai.errors import APIError

# --------------------------
# 1. الإعدادات والمفاتيح (لازم تغير السطرين دول)
# --------------------------
BOT_TOKEN = '8585706945:AAGaukgB6vMQWrjFFTvI-RI34yym5oMU4Sw' 
GEMINI_API_KEY = 'AIzaSyBbkfiKi11NmGqp8IC-qE_FZg24jpmPGTo' 

bot = telebot.TeleBot(BOT_TOKEN)

try:
    # تهيئة نموذج Gemini
    client = genai.Client(api_key=GEMINI_API_KEY)
    # اختيار النموذج المناسب للغة العربية والدردشة
    gemini_model = 'gemini-2.5-flash'
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    # ممكن نخليه يرد برسالة خطأ لو الـAPI مش شغال
    client = None

# ... (بقية الداتا والأزرار والدوال زي ما هي)
# (azkar_data و main_menu و send_welcome و callback_query)
# لأسباب الاختصار، نعتبر أن الدوال دي موجودة بالفعل

# --------------------------
# 6. معالج الرسائل النصية (Chatbot AI)
# --------------------------
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_ai_query(message):
    user_text = message.text
    chat_id = message.chat.id

    # نتأكد إن الرسالة مش أمر (/start مثلاً)
    if user_text.startswith('/'):
        return

    # نتأكد إن Gemini جاهز للعمل
    if client:
        try:
            # إرسال طلب لنموذج Gemini
            bot.send_chat_action(chat_id, 'typing') # لإظهار علامة "يكتب..."
            
            # يمكنك إضافة سياق للنظام ليكون أكثر التزامًا بالدين:
            # system_prompt = "أنت مساعد ذكي ومتحدث باللغة العربية. عند الإجابة على استفسارات دينية، كن حذرًا ومستندًا لآيات وأحاديث موثوقة قدر الإمكان."
            
            response = client.models.generate_content(
                model=gemini_model,
                contents=user_text,
                # config=genai.types.GenerateContentConfig(system_instruction=system_prompt)
            )
            
            bot.reply_to(message, response.text)

        except APIError as e:
            error_message = f"عفواً، حدث خطأ أثناء الاتصال بخدمة الذكاء الاصطناعي. (الخطأ: {e})"
            bot.reply_to(message, error_message)

        except Exception as e:
            error_message = f"حدث خطأ غير متوقع: {e}"
            bot.reply_to(message, error_message)
    else:
        # لو مفتاح Gemini فيه مشكلة
        bot.reply_to(message, "عذراً، خدمة الذكاء الاصطناعي غير متوفرة حالياً. يمكنك استخدام قوائم الأذكار.")

# --------------------------
# 7. تشغيل البوت
# --------------------------
# bot.infinity_polling() # شغل الدالة دي في النهاية زي ما عملنا قبل كده