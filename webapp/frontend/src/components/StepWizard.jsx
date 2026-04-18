import { Check } from 'lucide-react'

export default function StepWizard({ steps, currentStep, onStepClick }) {
  return (
    <div className="flex items-center justify-between bg-white rounded-xl p-4 shadow-sm border">
      {steps.map((step, index) => {
        const isActive = currentStep === step.id
        const isCompleted = currentStep > step.id

        return (
          <div key={step.id} className="flex items-center">
            <button
              onClick={() => onStepClick(step.id)}
              className={`flex items-center gap-3 ${
                isActive ? 'text-purple-600' : isCompleted ? 'text-green-600' : 'text-gray-400'
              }`}
            >
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold ${
                  isActive
                    ? 'bg-purple-100 text-purple-600'
                    : isCompleted
                    ? 'bg-green-100 text-green-600'
                    : 'bg-gray-100 text-gray-400'
                }`}
              >
                {isCompleted ? <Check className="w-5 h-5" /> : step.id}
              </div>
              <div className="text-left">
                <p className={`font-medium ${isActive ? 'text-purple-600' : ''}`}>{step.name}</p>
                <p className="text-xs text-gray-400">{step.description}</p>
              </div>
            </button>
            {index < steps.length - 1 && (
              <div className={`w-16 h-0.5 mx-4 ${isCompleted ? 'bg-green-500' : 'bg-gray-200'}`} />
            )}
          </div>
        )
      })}
    </div>
  )
}