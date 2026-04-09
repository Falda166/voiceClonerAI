import { CommonModule } from '@angular/common';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
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

  public text = 'Hallo, das ist eine geklonte Stimme.';
  public language = 'de';
  public audioFile?: File;
  public outputAudioUrl?: string;
  public loading = false;
  public error?: string;

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.audioFile = input.files[0];
      this.error = undefined;
    }
  }

  cloneVoice(): void {
    if (!this.audioFile) {
      this.error = 'Bitte zuerst eine Referenz-Audio auswählen.';
      return;
    }

    this.loading = true;
    this.error = undefined;

    const formData = new FormData();
    formData.append('reference_audio', this.audioFile);
    formData.append('text', this.text);
    formData.append('language', this.language);

    this.http.post('/api/clone', formData, { responseType: 'blob' }).subscribe({
      next: (blob) => {
        if (this.outputAudioUrl) {
          URL.revokeObjectURL(this.outputAudioUrl);
        }
        this.outputAudioUrl = URL.createObjectURL(blob);
        this.loading = false;
      },
      error: (err: HttpErrorResponse) => {
        if (err.status === 413) {
          this.error = 'Datei zu groß. Bitte kürzere/kleinere Referenz-Audio verwenden (Limit aktuell: 256 MB).';
        } else {
          this.error = err?.error?.detail ?? 'Klonen fehlgeschlagen. Prüfe Backend-Logs.';
        }
        this.loading = false;
      }
    });
  }
}
