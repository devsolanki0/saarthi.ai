"use client";

import { FormEvent, useState } from "react";
import { motion } from "framer-motion";
import { Send, Sparkles } from "lucide-react";

type Verse = {
  language: string;
  chapter_no: number;
  verse_no: number;
  question: string;
  answer: string;
  similarity_score: number;
};

type ChatResponse = {
  response?: string;
  verses?: Verse[];
  detail?: string;
};

const suggestions = [
  "I'm feeling lost about my career",
  "I'm afraid of failing",
  "I keep overthinking everything",
  "I'm struggling to let go",
];

export default function Chat() {
  const [message, setMessage] = useState("");
  const [answer, setAnswer] = useState("");
  const [verses, setVerses] = useState<Verse[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function sendMessage(text: string) {
    const cleanMessage = text.trim();

    if (!cleanMessage || loading) {
      return;
    }

    setLoading(true);
    setError("");
    setAnswer("");
    setVerses([]);

    try {
      console.log("SAARTHI.AI: Sending message...");
      console.log("Message:", cleanMessage);

      // IMPORTANT:
      // We use a relative URL.
      // Next.js will proxy /api/chat to FastAPI.
      const res = await fetch("/api/chat", {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          message: cleanMessage,
          top_k: 5,
        }),
      });

      console.log(
        "SAARTHI.AI HTTP status:",
        res.status
      );

      const rawText = await res.text();

      console.log(
        "SAARTHI.AI raw response:",
        rawText
      );

      let data: ChatResponse;

      try {
        data = JSON.parse(rawText);
      } catch {
        throw new Error(
          `SAARTHI.AI returned an invalid response. HTTP ${res.status}`
        );
      }

      if (!res.ok) {
        throw new Error(
          data.detail ||
            `SAARTHI.AI request failed with status ${res.status}`
        );
      }

      setAnswer(data.response || "");

      setVerses(
        Array.isArray(data.verses)
          ? data.verses
          : []
      );
    } catch (err) {
      console.error(
        "SAARTHI.AI request error:",
        err
      );

      if (err instanceof TypeError) {
        setError(
          "Unable to connect to SAARTHI.AI. Please make sure the backend is running."
        );
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError(
          "Something went wrong. Please try again."
        );
      }
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    const text = message.trim();

    if (!text) {
      return;
    }

    setMessage("");

    await sendMessage(text);
  }

  async function handleSuggestion(
    suggestion: string
  ) {
    await sendMessage(suggestion);
  }

  return (
    <main className="min-h-screen bg-[#080d18] text-white">
      <div className="relative min-h-screen overflow-hidden">

        {/* Background */}

        <div className="pointer-events-none absolute inset-0">

          <div
            className="
              absolute
              left-1/2
              top-[-220px]
              h-[550px]
              w-[550px]
              -translate-x-1/2
              rounded-full
              bg-blue-500/10
              blur-[130px]
            "
          />

          <div
            className="
              absolute
              bottom-[-200px]
              left-[-100px]
              h-[450px]
              w-[450px]
              rounded-full
              bg-purple-500/10
              blur-[130px]
            "
          />

        </div>

        {/* Header */}

        <header
          className="
            relative
            z-10
            border-b
            border-white/10
            bg-black/10
            backdrop-blur-xl
          "
        >
          <div
            className="
              mx-auto
              flex
              max-w-5xl
              items-center
              justify-between
              px-6
              py-5
            "
          >
            <div>
              <h1 className="text-xl font-semibold tracking-wide">
                SAARTHI
                <span className="text-blue-400">
                  .AI
                </span>
              </h1>

              <p className="mt-1 text-xs text-white/50">
                Ancient Wisdom. Modern Intelligence.
              </p>
            </div>

            <div className="flex items-center gap-2 text-xs text-white/50">
              <Sparkles size={14} />
              <span>Gita Companion</span>
            </div>
          </div>
        </header>

        {/* Main */}

        <section
          className="
            relative
            z-10
            mx-auto
            flex
            min-h-[calc(100vh-90px)]
            max-w-4xl
            flex-col
            px-6
            py-10
          "
        >

          {/* Intro */}

          <div className="mb-8 text-center">

            <motion.div
              initial={{
                opacity: 0,
                y: 15,
              }}
              animate={{
                opacity: 1,
                y: 0,
              }}
              transition={{
                duration: 0.6,
              }}
            >

              <h2 className="text-3xl font-semibold md:text-5xl">
                What is on your mind?
              </h2>

              <p
                className="
                  mx-auto
                  mt-4
                  max-w-2xl
                  text-sm
                  leading-6
                  text-white/55
                  md:text-base
                "
              >
                Share what you are going through.
                SAARTHI.AI will connect your situation
                with relevant teachings from the
                Bhagavad Gita and offer a practical
                reflection.
              </p>

            </motion.div>

          </div>

          {/* Suggestions */}

          {!answer && !loading && (

            <div
              className="
                mb-8
                flex
                flex-wrap
                justify-center
                gap-3
              "
            >

              {suggestions.map((suggestion) => (

                <button
                  key={suggestion}
                  type="button"
                  onClick={() =>
                    handleSuggestion(
                      suggestion
                    )
                  }
                  disabled={loading}
                  className="
                    rounded-full
                    border
                    border-white/10
                    bg-white/5
                    px-4
                    py-2
                    text-sm
                    text-white/70
                    transition
                    hover:border-blue-400/30
                    hover:bg-white/10
                    hover:text-white
                    disabled:cursor-not-allowed
                    disabled:opacity-40
                  "
                >
                  {suggestion}
                </button>

              ))}

            </div>

          )}

          {/* Loading */}

          {loading && (

            <motion.div
              initial={{
                opacity: 0,
              }}
              animate={{
                opacity: 1,
              }}
              className="
                mb-6
                flex
                items-center
                justify-center
                gap-3
                text-sm
                text-white/50
              "
            >

              <div
                className="
                  h-2
                  w-2
                  animate-pulse
                  rounded-full
                  bg-blue-400
                "
              />

              <span>
                Reflecting on the teachings of the Gita...
              </span>

            </motion.div>

          )}

          {/* Error */}

          {error && (

            <motion.div
              initial={{
                opacity: 0,
                y: 10,
              }}
              animate={{
                opacity: 1,
                y: 0,
              }}
              className="
                mb-6
                rounded-2xl
                border
                border-red-400/20
                bg-red-400/5
                p-4
                text-sm
                leading-6
                text-red-300
              "
            >
              {error}
            </motion.div>

          )}

          {/* AI Answer */}

          {answer && (

            <motion.div
              initial={{
                opacity: 0,
                y: 15,
              }}
              animate={{
                opacity: 1,
                y: 0,
              }}
              className="
                mb-6
                rounded-3xl
                border
                border-white/10
                bg-white/[0.04]
                p-6
                shadow-2xl
                backdrop-blur-xl
              "
            >

              <div
                className="
                  mb-4
                  flex
                  items-center
                  gap-2
                "
              >

                <Sparkles
                  size={18}
                  className="text-blue-400"
                />

                <span
                  className="
                    text-sm
                    font-medium
                    text-blue-300
                  "
                >
                  SAARTHI.AI
                </span>

              </div>

              <p
                className="
                  whitespace-pre-wrap
                  text-sm
                  leading-7
                  text-white/85
                  md:text-base
                "
              >
                {answer}
              </p>

            </motion.div>

          )}

          {/* Gita References */}

          {verses.length > 0 && (

            <motion.div
              initial={{
                opacity: 0,
              }}
              animate={{
                opacity: 1,
              }}
              className="mb-8"
            >

              <h3
                className="
                  mb-3
                  text-sm
                  font-medium
                  text-white/60
                "
              >
                Relevant Gita References
              </h3>

              <div className="grid gap-3">

                {verses.map(
                  (verse, index) => (

                    <div
                      key={`${verse.language}-${verse.chapter_no}-${verse.verse_no}-${index}`}
                      className="
                        rounded-2xl
                        border
                        border-white/10
                        bg-white/[0.03]
                        p-4
                      "
                    >

                      <div
                        className="
                          mb-2
                          flex
                          items-center
                          justify-between
                          gap-4
                        "
                      >

                        <span
                          className="
                            text-sm
                            font-medium
                            text-blue-300
                          "
                        >
                          Bhagavad Gita{" "}
                          {verse.chapter_no}.
                          {verse.verse_no}
                        </span>

                        <span
                          className="
                            text-xs
                            text-white/30
                          "
                        >
                          {verse.language}
                        </span>

                      </div>

                      <p
                        className="
                          text-xs
                          leading-5
                          text-white/45
                        "
                      >
                        {verse.answer}
                      </p>

                      <p
                        className="
                          mt-2
                          text-[11px]
                          text-white/25
                        "
                      >
                        Relevance:{" "}
                        {Number(
                          verse.similarity_score
                        ).toFixed(3)}
                      </p>

                    </div>

                  )
                )}

              </div>

            </motion.div>

          )}

          {/* Input */}

          <form
            onSubmit={handleSubmit}
            className="
              sticky
              bottom-6
              mt-auto
            "
          >

            <div
              className="
                flex
                items-center
                gap-3
                rounded-3xl
                border
                border-white/10
                bg-white/[0.06]
                p-2
                shadow-2xl
                backdrop-blur-xl
              "
            >

              <input
                type="text"
                value={message}
                onChange={(event) =>
                  setMessage(
                    event.target.value
                  )
                }
                placeholder="Share what is troubling you..."
                disabled={loading}
                className="
                  min-w-0
                  flex-1
                  bg-transparent
                  px-4
                  py-3
                  text-sm
                  text-white
                  outline-none
                  placeholder:text-white/30
                "
              />

              <button
                type="submit"
                disabled={
                  loading ||
                  !message.trim()
                }
                className="
                  flex
                  h-11
                  w-11
                  shrink-0
                  items-center
                  justify-center
                  rounded-full
                  bg-blue-500
                  text-white
                  transition
                  hover:bg-blue-400
                  disabled:cursor-not-allowed
                  disabled:opacity-30
                "
              >
                <Send size={18} />
              </button>

            </div>

            <p
              className="
                mt-3
                text-center
                text-[11px]
                text-white/25
              "
            >
              SAARTHI.AI is an AI companion inspired
              by the Bhagavad Gita, not a divine authority.
            </p>

          </form>

        </section>
      </div>
    </main>
  );
}