import {
  ApiErrorResponse,
  AuthResponse,
  HealthResponse,
  LoginRequest,
  PageResponse,
  PredictionHistoryItem,
  PredictionResponse,
  PropertyInputRequest,
  RegisterRequest,
  UserProfile,
} from '@/types/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8080';

export class ApiError extends Error {
  status: number;
  error: string;
  details?: Array<{ field: string; message: string }>;

  constructor(status: number, error: string, message: string, details?: Array<{ field: string; message: string }>) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.error = error;
    this.details = details;
  }
}

async function request<T>(endpoint: string, options: RequestInit = {}, token?: string | null): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    Accept: 'application/json',
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  let response: Response;
  try {
    response = await fetch(url, {
      ...options,
      headers,
    });
  } catch (err) {
    const errorMsg = err instanceof Error ? err.message : 'Network error';
    throw new ApiError(
      0,
      'NetworkError',
      `Unable to connect to PropValueAI service at ${API_BASE_URL}. Please ensure the backend is running. (${errorMsg})`
    );
  }

  if (!response.ok) {
    let errorData: ApiErrorResponse | null = null;
    try {
      errorData = await response.json();
    } catch {
      // response was not JSON
    }

    const status = response.status;
    const errorTitle = errorData?.error || response.statusText || 'Error';
    const errorMessage = errorData?.message || (status === 401 ? 'Authentication required. Please log in.' : status === 403 ? 'Access denied. You do not have permission for this resource.' : 'An unexpected error occurred.');

    throw new ApiError(status, errorTitle, errorMessage, errorData?.details);
  }

  return response.json();
}

export const api = {
  auth: {
    register: (data: RegisterRequest): Promise<UserProfile> =>
      request<UserProfile>('/api/v1/auth/register', {
        method: 'POST',
        body: JSON.stringify(data),
      }),

    login: (data: LoginRequest): Promise<AuthResponse> =>
      request<AuthResponse>('/api/v1/auth/login', {
        method: 'POST',
        body: JSON.stringify(data),
      }),

    me: (token: string): Promise<UserProfile> =>
      request<UserProfile>('/api/v1/auth/me', { method: 'GET' }, token),
  },

  predictions: {
    predict: (data: PropertyInputRequest, token: string): Promise<PredictionResponse> =>
      request<PredictionResponse>('/api/v1/predictions', {
        method: 'POST',
        body: JSON.stringify(data),
      }, token),

    getHistory: (page = 0, size = 10, token: string): Promise<PageResponse<PredictionHistoryItem>> =>
      request<PageResponse<PredictionHistoryItem>>(`/api/v1/predictions?page=${page}&size=${size}`, {
        method: 'GET',
      }, token),

    getById: (id: number, token: string): Promise<PredictionHistoryItem> =>
      request<PredictionHistoryItem>(`/api/v1/predictions/${id}`, {
        method: 'GET',
      }, token),
  },

  admin: {
    getAllPredictions: (page = 0, size = 10, token: string): Promise<PageResponse<PredictionHistoryItem>> =>
      request<PageResponse<PredictionHistoryItem>>(`/api/v1/admin/predictions?page=${page}&size=${size}`, {
        method: 'GET',
      }, token),
  },

  health: {
    check: (): Promise<HealthResponse> =>
      request<HealthResponse>('/api/v1/health', { method: 'GET' }),
  },
};
