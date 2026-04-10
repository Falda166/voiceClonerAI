import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  private readonly http = inject(HttpClient);

  token = '';
  username = 'admin';
  password = 'admin123!';
  cidr = '192.168.1.0/24';
  dryRun = true;

  devices: any[] = [];
  recommendations: any[] = [];
  auditLogs: any[] = [];
  status = 'Not connected';

  login(): void {
    this.http.post<any>('/api/v1/auth/login', { username: this.username, password: this.password }).subscribe({
      next: (resp) => {
        this.token = resp.access_token;
        this.status = 'Authenticated';
        this.refreshAll();
      },
      error: () => (this.status = 'Authentication failed')
    });
  }

  runDiscovery(): void {
    this.http
      .post<any>('/api/v1/discover/jobs', { cidr: this.cidr, dry_run: this.dryRun }, { headers: this.authHeaders() })
      .subscribe({
        next: (job) => {
          this.http
            .post(`/api/v1/discover/jobs/${job.id}/run`, {}, { headers: this.authHeaders() })
            .subscribe(() => this.refreshAll());
        },
        error: () => (this.status = 'Discovery failed')
      });
  }

  approve(recommendationId: number, approved: boolean): void {
    this.http
      .post(`/api/v1/recommendations/${recommendationId}/approve`, { approved }, { headers: this.authHeaders() })
      .subscribe(() => this.refreshAll());
  }

  refreshAll(): void {
    this.http.get<any[]>('/api/v1/discover/results', { headers: this.authHeaders() }).subscribe((x) => (this.devices = x));
    this.http.get<any[]>('/api/v1/recommendations', { headers: this.authHeaders() }).subscribe((x) => (this.recommendations = x));
    this.http.get<any[]>('/api/v1/audit-logs', { headers: this.authHeaders() }).subscribe((x) => (this.auditLogs = x));
  }

  private authHeaders(): HttpHeaders {
    return new HttpHeaders({ Authorization: `Bearer ${this.token}` });
  }
}
