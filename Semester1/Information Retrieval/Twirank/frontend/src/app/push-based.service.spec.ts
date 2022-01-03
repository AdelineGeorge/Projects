import { TestBed } from '@angular/core/testing';

import { PushBasedService } from './push-based.service';

describe('PushBasedService', () => {
  let service: PushBasedService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PushBasedService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
