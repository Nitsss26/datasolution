"use client"

export default function TestStylesPage() {
  return (
    <div className="min-h-screen bg-red-500 p-8">
      <div className="bg-blue-500 text-white p-4 rounded-lg shadow-lg">
        <h1 className="text-4xl font-bold mb-4">🎨 Tailwind CSS Test</h1>
        <p className="text-xl mb-6">If you can see colors and styling, Tailwind is working!</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div className="bg-green-500 p-4 rounded-lg text-center">
            <h3 className="text-xl font-bold">✅ Green Card</h3>
            <p>Background: bg-green-500</p>
          </div>
          <div className="bg-purple-600 p-4 rounded-lg text-center">
            <h3 className="text-xl font-bold">💜 Purple Card</h3>
            <p>Background: bg-purple-600</p>
          </div>
          <div className="bg-yellow-500 text-gray-900 p-4 rounded-lg text-center">
            <h3 className="text-xl font-bold">⚡ Yellow Card</h3>
            <p>Background: bg-yellow-500</p>
          </div>
          <div className="bg-pink-500 p-4 rounded-lg text-center">
            <h3 className="text-xl font-bold">🌸 Pink Card</h3>
            <p>Background: bg-pink-500</p>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 items-center justify-center">
          <button className="bg-white text-blue-600 px-6 py-3 rounded-lg font-bold hover:bg-gray-100 transition-colors">
            ✅ Primary Button
          </button>
          <button className="bg-green-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-700 transition-colors">
            🚀 Success Button
          </button>
          <button className="bg-red-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-red-700 transition-colors">
            ❌ Danger Button
          </button>
        </div>

        <div className="mt-8 p-4 bg-white text-gray-900 rounded-lg">
          <h2 className="text-2xl font-bold mb-2">📊 Test Results</h2>
          <ul className="space-y-1">
            <li>✅ Colors: Working</li>
            <li>✅ Typography: Working</li>
            <li>✅ Spacing: Working</li>
            <li>✅ Borders: Working</li>
            <li>✅ Shadows: Working</li>
            <li>✅ Responsive: Working</li>
          </ul>
        </div>
      </div>
    </div>
  )
}