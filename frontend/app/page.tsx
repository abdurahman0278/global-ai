import ComparisonForm from '@/components/ComparisonForm';
import ComparisonHistory from '@/components/ComparisonHistory';

export default function Home() {
  return (
    <main className="min-h-screen py-12 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">GlobalAI Data Comparison Platform</h1>
          <p className="text-gray-600">
            AI-powered similarity scoring between structured form data and handwritten images
          </p>
        </div>

        <div className="mb-12">
          <ComparisonForm />
        </div>

        <div>
          <ComparisonHistory />
        </div>
      </div>
    </main>
  );
}

