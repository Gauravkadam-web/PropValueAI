export interface UserProfile {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: 'ROLE_USER' | 'ROLE_ADMIN';
  created_at: string;
}

export interface AuthResponse {
  token: string;
  type: string;
  expires_in: number;
  user: UserProfile;
}

export interface RegisterRequest {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface PropertyInputRequest {
  total_sqft: number;
  size: string;
  bath: number;
  balcony: number;
  area_type: string;
}

export interface PredictionResponse {
  id: number;
  predicted_price: number;
  target_unit: string;
  model_name: string;
  model_version: string;
  fastapi_prediction_id: string;
  disclaimer: string;
  created_at: string;
}

export interface PredictionHistoryItem {
  id: number;
  total_sqft: string;
  size: string | null;
  bath: number | null;
  balcony: number | null;
  area_type: string | null;
  predicted_price: number;
  target_unit: string;
  model_name: string;
  model_version: string;
  disclaimer: string;
  status: string;
  created_at: string;
}

export interface PageResponse<T> {
  content: T[];
  page: number;
  size: number;
  total_elements: number;
  total_pages: number;
  last: boolean;
}

export interface ApiErrorDetail {
  field: string;
  message: string;
}

export interface ApiErrorResponse {
  status: number;
  error: string;
  message: string;
  path: string;
  timestamp?: string;
  details?: ApiErrorDetail[];
}

export interface HealthResponse {
  timestamp: string;
  service: string;
  status: string;
  components: {
    database: {
      status: string;
      type?: string;
      error?: string;
    };
    inference_service: {
      status: string;
      ready: boolean;
    };
  };
}
