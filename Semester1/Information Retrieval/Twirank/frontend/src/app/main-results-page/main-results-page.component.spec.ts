import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MainResultsPageComponent } from './main-results-page.component';

describe('MainResultsPageComponent', () => {
  let component: MainResultsPageComponent;
  let fixture: ComponentFixture<MainResultsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MainResultsPageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MainResultsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
