'use client';

import React, { useState } from 'react';
import { AppShell } from '@/components/layout/AppShell';
import { Card, CardHeader } from '@/components/ui/Card';
import { PredictionForm } from '@/components/prediction/PredictionForm';
import { PredictionResultCard } from '@/components/prediction/PredictionResultCard';
import { PredictionResponse } from '@/types/api';

export default function NewPredictionPage() {
  const [predictionResult, setPredictionResult] = useState<PredictionResponse | null>(null);

  return (
    <AppShell title="New Property Valuation">
      <div className="max-w-4xl mx-auto space-y-6">
        {!predictionResult ? (
          <Card>
            <CardHeader
              title="Estimate Residential Property Price"
              subtitle="Enter property attributes to compute machine learning valuation via fitted Random Forest regressor."
            />
            <PredictionForm onSuccess={(result) => setPredictionResult(result)} />
          </Card>
        ) : (
          <PredictionResultCard
            result={predictionResult}
            onReset={() => setPredictionResult(null)}
          />
        )}
      </div>
    </AppShell>
  );
}
