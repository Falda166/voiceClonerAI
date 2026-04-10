import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  private readonly http = inject(HttpClient);

  token = '';
  username = 'admin';
  password = 'admin123';
  cidr = '192.168.1.0/24';
  message = 'Login required';
  devices: Array<{uid: string; ip: string; confidence: number}> = [];
  auditLogs: Array<{action: string; target: string}> = [];

  private authHeaders(): HttpHeaders {
    return new HttpHeaders({ Authorization: `Bearer ${this.token}` });
  }

  login(): void {
    this.http.post<{access_token: string}>('/api/v1/auth/login', {
      username: this.username,
      password: this.password
    }).subscribe({
      next: (response) => {
        this.token = response.access_token;
        this.message = 'Authenticated as admin';
      },
      error: () => this.message = 'Login failed'
    });
  }

  runDiscovery(): void {
    this.http.post<{status: string; findings: number}>('/api/v1/discovery/jobs', {
      scope_cidr: this.cidr,
      dry_run: false,
      plugins: ['mdns', 'ssdp']
    }, { headers: this.authHeaders() }).subscribe({
      next: (result) => this.message = `Discovery ${result.status} (${result.findings} findings)`,
      error: () => this.message = 'Discovery failed'
    });
  }

  loadDevices(): void {
    this.http.get<Array<{uid: string; ip: string; confidence: number}>>('/api/v1/devices', { headers: this.authHeaders() }).subscribe({
      next: (data) => this.devices = data,
      error: () => this.message = 'Could not load devices'
    });
  }

  loadAuditLogs(): void {
    this.http.get<Array<{action: string; target: string}>>('/api/v1/audit-logs', { headers: this.authHeaders() }).subscribe({
      next: (data) => this.auditLogs = data,
      error: () => this.message = 'Could not load audit logs'
    });
  }
}
