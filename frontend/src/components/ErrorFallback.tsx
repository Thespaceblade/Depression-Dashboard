import { FaGithub, FaLinkedin } from 'react-icons/fa';

interface ErrorFallbackProps {
  error: string;
  onRetry: () => void;
}

export default function ErrorFallback({ error, onRetry }: ErrorFallbackProps) {
  const githubUrl = 'https://github.com/Thespaceblade/Depression-Dashboard';
  const portfolioUrl = 'https://jasonindata.vercel.app';
  const linkedinUrl = 'https://www.linkedin.com/in/jasoncharwin';

  return (
    <div className="min-h-screen bg-field text-ink">
      <div className="max-w-xl mx-auto px-4 sm:px-6 py-16 sm:py-24 animate-flood-in">
        <p className="label-caps text-loss mb-3">Service unavailable</p>
        <h1 className="font-display text-4xl sm:text-5xl uppercase tracking-wide leading-tight mb-4">
          Depression
          <br />
          Dashboard
        </h1>
        <p className="text-muted leading-relaxed mb-6">
          The API is down or unreachable. Retry in a moment, or open the project while the feed recovers.
        </p>

        <p className="font-mono text-sm text-loss border border-line border-l-led border-l-2 pl-3 py-3 mb-8">
          {error}
        </p>

        <button type="button" onClick={onRetry} className="util-btn mb-10">
          Try again
        </button>

        <div className="section-rule pt-8 space-y-3">
          <p className="label-caps mb-3">Elsewhere</p>
          <a href={githubUrl} target="_blank" rel="noopener noreferrer" className="util-link flex items-center gap-2">
            <FaGithub size={14} /> GitHub
          </a>
          <a href={portfolioUrl} target="_blank" rel="noopener noreferrer" className="util-link block">
            Portfolio
          </a>
          <a href={linkedinUrl} target="_blank" rel="noopener noreferrer" className="util-link flex items-center gap-2">
            <FaLinkedin size={14} /> LinkedIn
          </a>
        </div>

        <p className="mt-12 label-caps">Built by Jason Charwin</p>
      </div>
    </div>
  );
}
