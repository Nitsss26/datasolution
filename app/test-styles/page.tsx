"use client"

export default function TestStylesPage() {
  return (
    <div className="min-h-screen bg-red-500 p-8">
      <div className="bg-blue-500 text-white p-4 rounded-lg">
        <h1 className="text-4xl font-bold mb-4">Tailwind CSS Test</h1>
        <p className="text-lg">If you can see colors and styling, Tailwind is working!</p>
        <div className="mt-4 space-y-2">
          <div className="bg-green-500 p-2 rounded">Green background</div>
          <div className="bg-yellow-500 p-2 rounded">Yellow background</div>
          <div className="bg-purple-500 p-2 rounded">Purple background</div>
        </div>
        <button className="mt-4 bg-white text-black px-4 py-2 rounded hover:bg-gray-200">
          Test Button
        </button>
      </div>
    </div>
  )
}