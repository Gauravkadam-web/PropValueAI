'use client';

import React, { useState } from 'react';
import { useAuth } from '@/lib/auth/AuthContext';
import { api, ApiError } from '@/lib/api/client';
import { PredictionResponse, PropertyInputRequest } from '@/types/api';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Button } from '@/components/ui/Button';
import { Alert } from '@/components/ui/Alert';
import { CalculatorIcon } from '@/components/ui/Icons';

interface PredictionFormProps {
  onSuccess: (result: PredictionResponse) => void;
}

const AREA_TYPE_OPTIONS = [
  { value: 'Super built-up  Area', label: 'Super built-up Area' },
  { value: 'Plot  Area', label: 'Plot Area' },
  { value: 'Built-up  Area', label: 'Built-up Area' },
  { value: 'Carpet  Area', label: 'Carpet Area' },
];

const BHK_OPTIONS = [
  { value: '1 BHK', label: '1 BHK' },
  { value: '2 BHK', label: '2 BHK' },
  { value: '3 BHK', label: '3 BHK' },
  { value: '4 BHK', label: '4 BHK' },
  { value: '5 BHK', label: '5 BHK' },
];

export function PredictionForm({ onSuccess }: PredictionFormProps) {
  const { token } = useAuth();
  const [totalSqft, setTotalSqft] = useState<string>('1200');
  const [size, setSize] = useState<string>('2 BHK');
  const [bath, setBath] = useState<string>('2');
  const [balcony, setBalcony] = useState<string>('1');
  const [areaType, setAreaType] = useState<string>('Super built-up  Area');

  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});

  function validate(): boolean {
    const errors: Record<string, string> = {};

    const sqftVal = parseFloat(totalSqft);
    if (isNaN(sqftVal) || sqftVal <= 0) {
      errors.totalSqft = 'Total square footage must be a positive number (e.g., 1200).';
    } else if (sqftVal > 50000) {
      errors.totalSqft = 'Total square footage must be realistic (50,000 max).';
    }

    const bathVal = parseFloat(bath);
    if (isNaN(bathVal) || bathVal < 1 || bathVal > 15) {
      errors.bath = 'Bathrooms must be between 1 and 15.';
    }

    const balconyVal = parseFloat(balcony);
    if (isNaN(balconyVal) || balconyVal < 0 || balconyVal > 10) {
      errors.balcony = 'Balconies must be between 0 and 10.';
    }

    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setFormError(null);

    if (!token) {
      setFormError('Authentication session expired. Please sign in again.');
      return;
    }

    if (!validate()) {
      return;
    }

    setIsLoading(true);

    const payload: PropertyInputRequest = {
      total_sqft: parseFloat(totalSqft),
      size: size.trim(),
      bath: parseFloat(bath),
      balcony: parseFloat(balcony),
      area_type: areaType,
    };

    try {
      const response = await api.predictions.predict(payload, token);
      onSuccess(response);
    } catch (err) {
      if (err instanceof ApiError) {
        setFormError(err.message);
      } else {
        setFormError('An unexpected error occurred while contacting the prediction engine.');
      }
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {formError && (
        <Alert variant="danger" title="Valuation Request Failed">
          {formError}
        </Alert>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {/* Total Square Feet */}
        <Input
          label="Total Square Feet (Area)"
          type="number"
          step="any"
          required
          min="1"
          max="50000"
          value={totalSqft}
          onChange={(e) => setTotalSqft(e.target.value)}
          error={fieldErrors.totalSqft}
          helperText="E.g., 1200 for a 2 BHK apartment in Pune."
          placeholder="1200"
        />

        {/* Configuration / Bedrooms */}
        <Select
          label="Configuration (Size)"
          required
          value={size}
          onChange={(e) => setSize(e.target.value)}
          options={BHK_OPTIONS}
          helperText="Residential room configuration."
        />

        {/* Bathroom Count */}
        <Input
          label="Bathroom Count"
          type="number"
          required
          min="1"
          max="15"
          value={bath}
          onChange={(e) => setBath(e.target.value)}
          error={fieldErrors.bath}
          helperText="Number of bathrooms (1 - 15)."
          placeholder="2"
        />

        {/* Balcony Count */}
        <Input
          label="Balcony Count"
          type="number"
          required
          min="0"
          max="10"
          value={balcony}
          onChange={(e) => setBalcony(e.target.value)}
          error={fieldErrors.balcony}
          helperText="Number of balconies (0 - 10)."
          placeholder="1"
        />

        {/* Area Type */}
        <div className="md:col-span-2">
          <Select
            label="Property Area Type"
            required
            value={areaType}
            onChange={(e) => setAreaType(e.target.value)}
            options={AREA_TYPE_OPTIONS}
            helperText="Classification specified in property deeds."
          />
        </div>
      </div>

      <div className="pt-2">
        <Button
          type="submit"
          variant="primary"
          size="lg"
          isLoading={isLoading}
          className="w-full sm:w-auto"
        >
          <CalculatorIcon className="w-5 h-5" />
          Estimate Property Price
        </Button>
      </div>
    </form>
  );
}
