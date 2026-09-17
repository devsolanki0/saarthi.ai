"use client";

import Image from "next/image";
import { motion } from "framer-motion";
import { ArrowRight, BookOpen, Heart, Sparkles, Sprout } from "lucide-react";

interface LandingProps {
  onBegin: () => void;
}

export default function Landing({ onBegin }: LandingProps) {
  return (
    <main className="min-h-screen overflow-hidden bg-[#070b12] text-white">
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <motion.div
          animate={{ scale: [1, 1.08, 1], opacity: [0.08, 0.16, 0.08] }}
          transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
          className="absolute left-[65%] top-[35%] h-[520px] w-[520px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-amber-400/20 blur-[120px]"
        />
        {[...Array(18)].map((_, i) => (
          <motion.span
            key={i}
            animate={{ y: [0, -20, 0], opacity: [0.15, 0.5, 0.15] }}
            transition={{ duration: 3 + (i % 4), repeat: Infinity, delay: i * 0.25 }}
            className="absolute h-1 w-1 rounded-full bg-amber-200"
            style={{ left: `${5 + ((i * 17) % 90)}%`, top: `${10 + ((i * 29) % 75)}%` }}
          />
        ))}
      </div>

      <nav className="relative z-10 mx-auto flex max-w-7xl items-center justify-between px-6 py-6 md:px-10">
        <div className="flex items-center gap-3">
          <span className="text-2xl">🦚</span>
          <span className="font-semibold tracking-[0.18em]">SAARTHI.AI</span>
        </div>
        <div className="hidden text-xs tracking-[0.2em] text-white/35 sm:block">
          ANCIENT WISDOM · MODERN INTELLIGENCE
        </div>
      </nav>

      <section className="relative z-10 mx-auto grid min-h-[calc(100vh-88px)] max-w-7xl items-center gap-10 px-6 pb-12 md:grid-cols-2 md:px-10">
        <div className="max-w-2xl">
          <motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} className="mb-6 inline-flex items-center gap-2 rounded-full border border-amber-300/15 bg-amber-300/5 px-4 py-2 text-xs text-amber-200/75">
            <Sparkles size={14} /> Ancient Wisdom · Modern Intelligence
          </motion.div>

          <motion.h1 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="text-5xl font-light leading-[1.05] tracking-tight md:text-7xl">
            When life feels
            <span className="block text-amber-200">uncertain...</span>
          </motion.h1>

          <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.25 }} className="mt-7 max-w-xl text-base leading-8 text-white/45 md:text-lg">
            Pause. Reflect. Find a clearer path through timeless teachings inspired by the Bhagavad Gita.
          </motion.p>

          <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="mt-9 flex flex-wrap gap-3">
            <button onClick={onBegin} className="group flex items-center gap-3 rounded-full bg-amber-300 px-6 py-3.5 font-medium text-black transition hover:bg-amber-200">
              Begin your journey <ArrowRight size={18} className="transition group-hover:translate-x-1" />
            </button>
            <button className="flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-6 py-3.5 text-white/70 hover:bg-white/10">
              <BookOpen size={17} /> Explore the Gita
            </button>
          </motion.div>

          <div className="mt-12 grid max-w-xl grid-cols-3 gap-3">
            {[
              [Heart, "Reflect"],
              [BookOpen, "Discover"],
              [Sprout, "Grow"]
            ].map(([Icon, label]) => (
              <div key={label as string} className="rounded-2xl border border-white/8 bg-white/4 p-4">
                <Icon size={18} className="mb-3 text-amber-300/75" />
                <div className="text-sm text-white/65">{label as string}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="relative mx-auto h-[560px] w-full max-w-[540px] md:h-[680px]">
          <motion.div animate={{ scale: [1, 1.04, 1], opacity: [0.15, 0.25, 0.15] }} transition={{ duration: 6, repeat: Infinity }} className="absolute inset-[12%] rounded-full bg-amber-300/20 blur-[70px]" />
          <motion.div animate={{ rotate: 360 }} transition={{ duration: 45, repeat: Infinity, ease: "linear" }} className="absolute inset-[10%] rounded-full border border-amber-200/10" />
          <motion.div animate={{ y: [0, -10, 0] }} transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }} className="absolute inset-0">
            <Image src="/images/krishna/saarthi-krishna.png" alt="Krishna playing the flute beside the river" fill priority sizes="(max-width: 768px) 100vw, 50vw" className="object-contain drop-shadow-[0_30px_60px_rgba(0,0,0,0.45)]" />
          </motion.div>
        </div>
      </section>
    </main>
  );
}