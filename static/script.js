
const chatInput = document.querySelector('.chat-input textarea');
//const sendChatBtn = document.querySelector('.chat-input button');
const sendChatBtn = document.getElementById('sendBTN');
const uploadBtn = document.getElementById('uploadBTN');
const uploadedFile = document.getElementById('fileid');
const chatbox = document.querySelector(".chatbox");

let userMessage;

const createChatLi = (message, className) => {
	const chatLi = document.createElement("li");
	chatLi.classList.add("chat", className);
	let chatContent =
		className === "chat-outgoing" ? `<p>${message}</p>` : `<p>${message}</p>`;
	chatLi.innerHTML = chatContent;
	return chatLi;
}

async function uploadFile() {
    let formData = new FormData();
		formData.append("file", uploadedFile.files[0]);
		await fetch('/', {
		    method: "POST",
		    body: formData
		});
	alert("File uploaded successfully");
}

const generateResponse = (incomingChatLi) => {
		const messageElement = incomingChatLi.querySelector("p");
		$.ajax({
		    url: '/',
		    type: 'POST',
		    contentType: 'application/json',
            data: JSON.stringify({ 'data': userMessage }),
                success: function(response) {
                    messageElement.textContent = response.output;
                },
                error: function(error) {
                    console.log(error);
                }
		});
};


const handleChat = () => {
	userMessage = chatInput.value.trim();
	if (!userMessage) {
		return;
	}
	chatbox.appendChild(createChatLi(userMessage, "chat-outgoing"));
	chatbox.scrollTo(0, chatbox.scrollHeight);
	chatInput.value = ""

	setTimeout(() => {
		const incomingChatLi = createChatLi("Thinking...", "chat-incoming")
		chatbox.appendChild(incomingChatLi);
		chatbox.scrollTo(0, chatbox.scrollHeight);
		generateResponse(incomingChatLi);
	}, 600);
}

sendChatBtn.addEventListener("click", handleChat);
uploadBtn.addEventListener("click", uploadFile);

function cancel() {
	let chatbotcomplete = document.querySelector(".chatBot");
	if (chatbotcomplete.style.display != 'none') {
		chatbotcomplete.style.display = "none";
		let lastMsg = document.createElement("p");
		lastMsg.textContent = 'Thanks for using our Chatbot!';
		lastMsg.classList.add('lastMessage');
		document.body.appendChild(lastMsg)
	}
}
