"use client";

import { AnimatePresence, motion } from "framer-motion";
import { useState } from "react";
import Landing from "@/components/Landing";
import Chat from "@/components/Chat";

export default function Home() {
  const [started, setStarted] = useState(false);

  return (
    <AnimatePresence mode="wait">
      {!started ? (
        <motion.div
          key="landing"
          initial={{ opacity: 1 }}
          exit={{ opacity: 0, scale: 1.03 }}
          transition={{ duration: 0.8, ease: "easeInOut" }}
        >
          <Landing onBegin={() => setStarted(true)} />
        </motion.div>
      ) : (
        <motion.div
          key="chat"
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.9, ease: "easeOut" }}
        >
          <Chat />
        </motion.div>
      )}
    </AnimatePresence>
  );
}