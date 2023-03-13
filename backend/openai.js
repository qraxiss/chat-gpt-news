const { Configuration, OpenAIApi } = require("openai");

const configuration = new Configuration({
    apiKey: "Your Api Key",
});
const openai = new OpenAIApi(configuration);

const base_messages = [
    { role: "user", content: "Merhaba, sana vereceğim kripto haberlerini değerlendirir misin?" },
    { role: "assistant", content: 'Yorumlamak için heycanla vereceğin haberleri bekliyorum! Verdiğin haberleri 2 şekilde yorumlayacağım. İlk olarak haberin etkisini 1 ila 10 arasında yorumlayacağım. 1: piyasaya bir etkisi olmaz 10: piyasaya çok etkisi olur.İkinci olarak haberin yönü, piyasayı negatif mi etkiler, pozitif mi etkiler.' },
    { role: "user", content: "Verdiğim haberlere yanıtı json şeklinde verebilir misin?"},
    { role: 'assistant', content: 'Tabi, haberlere şu formatta yanıt vereceğim: ğer haber niteliği taşıyorsa mesaj formatım şöyle olacak {"puan": <etkisi>,"yon": "<yönü>","ai_opinion": "<yorumum>"}'},
    { role: "user", content: "Lütfen JSON Parse etmemi engelleyecek bir biçimde cevap verme."},
    { role: "assistant", content: '{"puan": 1, "yon": pozitif, "ai_opinion":"Tabi, haberlere bu formatta cevap vereceğim"}'},
    { role: "user", content: 'Ve eklemem gerekirse eğer sana attığım metin bir haber değilse dönüş formatın şu olsun: {"puan": 1, "yon": "nötr", "ai_opinion":"<yorumum>"}'},
    { role: "user", content: "Ve yorumun maksimum 120 kelime olsun."}

]

async function getOpinion(news) {
        messages = [...base_messages]
        messages.push({
                role: "user",
                content: news
            }
        );
        const completion = await openai.createChatCompletion({
            model: "gpt-3.5-turbo",
            messages: messages,
        });
        
        return {
            content:completion.data.choices[0].message.content,
            total_tokens:completion.data.usage.total_tokens
        }
}

module.exports = {
    getOpinion
}
