import axios from 'axios';
import type { Opportunity } from '$types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export async function fetchOpportunities(): Promise<Opportunity[]> {
  try {
    const response = await axios.get<Opportunity[]>(`${API_BASE_URL}/opportunities`);
    return response.data;
  } catch (error) {
    console.error('Error fetching opportunities:', error);
    throw error;
  }
}

export async function createOpportunity(opportunity: Partial<Opportunity>): Promise<Opportunity> {
  try {
    const response = await axios.post<Opportunity>(`${API_BASE_URL}/opportunities`, opportunity);
    return response.data;
  } catch (error) {
    console.error('Error creating opportunity:', error);
    throw error;
  }
}