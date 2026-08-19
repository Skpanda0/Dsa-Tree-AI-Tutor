export async function POST(request) {
  try {
    const { code, output, question, language } = await request.json();

    if (!code?.trim()) {
      return Response.json({ answer: "Write some code first, then ask me about it." });
    }

    const q = (question || "").toLowerCase();

    if (q.includes("complex") || q.includes("time")) {
      return Response.json({
        answer: `I can analyze the time and space complexity of your ${language || "code"}. Look at loops, nested loops, and recursive calls. For an exact analysis, tell me which function you want to focus on.`
      });
    }

    if (output?.toLowerCase?.().includes("error") || output?.toLowerCase?.().includes("exception")) {
      return Response.json({
        answer:
          "Your latest execution contains an error. Start with the first error or exception line and inspect the referenced line number. I can walk through the fix step by step."
      });
    }

    return Response.json({
      answer:
        "I can help you debug this step by step. Run the code first, then ask me what you want to understand. This tutor endpoint is ready to be connected to an LLM."
    });
  } catch {
    return Response.json(
      { answer: "I couldn't process that tutor request." },
      { status: 400 }
    );
  }
}