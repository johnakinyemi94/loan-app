import { ApplicationForm } from "@/app/components/ApplicationForm";

export default function Home() {
  return (
    <main className="relative flex-1 overflow-hidden px-5 py-8 sm:px-8 lg:px-12 lg:py-12">
      <div className="pointer-events-none absolute -right-24 -top-32 h-80 w-80 rounded-full bg-lime-200/50 blur-3xl" />
      <div className="pointer-events-none absolute -bottom-40 -left-24 h-96 w-96 rounded-full bg-sky-100/70 blur-3xl" />

      <div className="relative mx-auto max-w-7xl">
        <header className="mb-10 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-950 text-sm font-bold text-lime-300 shadow-lg shadow-slate-950/20">LA</div>
            <div>
              <p className="text-sm font-bold tracking-tight text-slate-950">Lendwise</p>
              <p className="text-xs font-medium text-slate-500">Approval desk</p>
            </div>
          </div>
          <span className="hidden rounded-full border border-slate-200 bg-white/70 px-4 py-2 text-xs font-semibold text-slate-600 sm:block">Secure application portal</span>
        </header>

        <section className="grid gap-10 lg:grid-cols-[minmax(0,0.78fr)_minmax(0,1.22fr)] lg:items-start">
          <div className="max-w-xl lg:sticky lg:top-8">
            <p className="mb-5 flex items-center gap-2 text-xs font-bold uppercase tracking-[0.2em] text-sky-700"><span className="h-2 w-2 rounded-full bg-lime-400" />Personal lending</p>
            <h1 className="max-w-lg text-5xl font-semibold leading-[0.98] tracking-[-0.045em] text-slate-950 sm:text-6xl">A clearer path to your next move.</h1>
            <p className="mt-6 max-w-md text-base leading-7 text-slate-600 sm:text-lg">Share a few details and we&apos;ll review your application with a transparent, human-readable decision.</p>

            <div className="mt-10 border-t border-slate-200/80 pt-6">
              <p className="text-xs font-bold uppercase tracking-[0.18em] text-slate-400">What happens next</p>
              <div className="mt-5 space-y-5">
                <div className="flex gap-4">
                  <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-slate-950 text-xs font-bold text-lime-300">01</span>
                  <div><p className="font-semibold text-slate-900">We review your profile</p><p className="mt-1 text-sm leading-6 text-slate-500">A quick assessment based on the information you provide.</p></div>
                </div>
                <div className="flex gap-4">
                  <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-sky-100 text-xs font-bold text-sky-700">02</span>
                  <div><p className="font-semibold text-slate-900">You get a clear answer</p><p className="mt-1 text-sm leading-6 text-slate-500">See your decision, confidence, and next steps in one place.</p></div>
                </div>
              </div>
            </div>
          </div>

          <ApplicationForm />
        </section>

      <footer className="mt-12 flex flex-col gap-2 border-t border-slate-200/80 pt-5 text-xs text-slate-400 sm:flex-row sm:items-center sm:justify-between"><span>Your information is encrypted and handled securely.</span><span>Usually takes less than 3 minutes</span></footer>
      </div>
    </main>
  );
}
